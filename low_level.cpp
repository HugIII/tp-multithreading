#include <chrono>
#include <iostream>
#include <stdio.h>
#include <string>

#include <Eigen/Dense>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

using Eigen::MatrixXf;
using namespace std;
using json = nlohmann::json;

class Task {
public:
  Task(int size, MatrixXf a, MatrixXf b, int identifier);
  void work();
  string encodeJson();

private:
  int size;
  MatrixXf a;
  Eigen::VectorXf b;
  Eigen::VectorXf x;
  int identifier;
  float time;
};

Task::Task(int size, MatrixXf a, MatrixXf b, int identifier)
    : a(a), b(b), identifier(identifier), size(size) {
  float time = 0;
  x = Eigen::VectorXf(size);
}

Task decodeJson(string s) {
  // il faut decode le fichier Json
  json j = json::parse(s);

  int size_temp = int(j["size"]);

  MatrixXf a_temp = MatrixXf(size_temp, size_temp);
  Eigen::VectorXf b_temp = Eigen::VectorXf(size_temp);

  for (int i = 0; i < size_temp; i++) {
    for (int j_idx = 0; j_idx < size_temp; j_idx++) {
      a_temp(i, j_idx) = j["a"][i][j_idx];
    }
  }

  for (int i = 0; i < size_temp; i++) {
    b_temp(i) = j["b"][i];
  }

  int identifier_temp = int(j["identifier"]);

  Task t = Task(size_temp, a_temp, b_temp, identifier_temp);
  return t;
}

string Task::encodeJson() {
  // il faut encode le fichier Json
  json j;
  j["size"] = size;
  j["identifier"] = identifier;

  for (int i = 0; i < size; i++) {
    j["b"][i] = b[i];
    j["x"][i] = x[i];
    for (int k = 0; k < size; k++) {
      j["a"][i][k] = a(i, k);
    }
  }

  j["time"] = time;
  return j.dump();
}

void Task::work() {
  auto start = chrono::steady_clock::now();
  x = a.householderQr().solve(b);
  auto end = chrono::steady_clock::now();
  time = std::chrono::duration<float>(end - start).count();
}

class Minion {
public:
  Minion();
  void get();

private:
  void put(string s);
};

Minion::Minion() {}

void Minion::get() {
  // il faut voir s'il y a des taches en attentes
  cpr::Response r = cpr::Get(cpr::Url{"127.0.0.1:8000"});

  if (r.status_code == 200) {
    Task t = decodeJson(r.text);
    t.work();
    string s = t.encodeJson();
    put(s);
  }
}

void Minion::put(string s) {
  // il faut renvoyer la task et le resultat
  cpr::Post(cpr::Url{"127.0.0.1:8000"}, cpr::Body{s});
}

int main(int argc, char **argv) {
  Eigen::setNbThreads(4);
  Minion *m = new Minion();
  while (1) {
    m->get();
  }
}
