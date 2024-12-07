/*
 * File name: low_level.cpp
 * Author:    Clara Baffogne, Hugo Blayes
 * Date:      06/12/24
 * Description: This file is the C++ version of Minion.py, it retrieves the
 * tasks to do from the QueueManager thanks to the Proxy. It will then solve the
 * task, storing the result and the time it took the task to execute. Once the
 * task has been completed, it is sent back to the QueueManager via the Web
 * Proxy server.
 */

// Include
// Standard////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <chrono>
#include <iostream>
#include <stdio.h>
#include <string>

// Include Library
// ///////////////////////////////////////////////////////////////////////////////////////////////////////
#include <Eigen/Dense>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

// Using
// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Shorten object names
using Eigen::MatrixXf;
using namespace std;
using json = nlohmann::json;

// Class Task
// ////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Task {
  // This class is the equivalent of task.py in C++
public:
  // Constructor
  Task(int size, MatrixXf a, MatrixXf b, int identifier);

  // Method
  void work();
  string encodeJson();

private:
  // Attribute
  int size;
  int identifier;
  float time;
  MatrixXf a;        // Dimension 2
  Eigen::VectorXf b; // Dimension 1
  Eigen::VectorXf x; // Dimension 1
};

Task::Task(int size, MatrixXf a, MatrixXf b, int identifier)
    : a(a), b(b), identifier(identifier), size(size) {
  // Constructor
  float time = 0;
  x = Eigen::VectorXf(size);
}

Task decodeJson(string s) {
  // This function transforms a json into the task object
  json j = json::parse(s);

  // we first retrieve the size, which defines the size of our matrices
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

  // Finally, we create the object in order to pass it via return
  Task t = Task(size_temp, a_temp, b_temp, identifier_temp);
  return t;
}

string Task::encodeJson() {
  // This function can be used to pass a task in json format

  // Our json object
  json j;

  // In json, the order of our objects doesn't really matter, so we put easy
  // objects first
  j["size"] = size;
  j["identifier"] = identifier;
  j["time"] = time;

  // Since b and x are vectors of size 'size', we can easily assign each field
  // of our json with a for
  for (int i = 0; i < size; i++) {
    j["b"][i] = b[i];
    j["x"][i] = x[i];
    // For a it's a bit different, as it's a sizexsize matrix, we have to use
    // two nested loops to assign each value of our matrix in the json
    for (int k = 0; k < size; k++) {
      j["a"][i][k] = a(i, k);
    }
  }

  // dump transforms the json object into a string,
  // since the json object is intended to be sent unchanged at the output of
  // this line, dump allows the object to be better prepared for sending
  return j.dump();
}

void Task::work() {
  // This function solves the equation for our task,
  // measuring the time taken to solve it and displaying for debugging purposes
  // that the task has been completed

  // have the task start time
  auto start = chrono::steady_clock::now();

  // To solve the task, we decided to use the householderQr function,
  // because compared to other eigenfunctions, it works with all matrices,
  // and it represents the balance between efficiency between small and large
  // matrices, and accuracy
  x = a.householderQr().solve(b);

  // have the task end time
  auto end = chrono::steady_clock::now();

  // the difference is the time it took to complete the task
  time = std::chrono::duration<float>(end - start).count();

  // the user is informed that the task is finished
  cout << "La tâche " << identifier << " a été effectué " << endl;
}

// Class Minion
// //////////////////////////////////////////////////////////////////////////////////////////////////////////

class Minion {
  // This class is the equivalent of Minion.py
  // This class is used to receive tasks from the proxy and to perform the tasks
  // in order to obtain the results
public:
  // constructor
  Minion();

  // method
  void get();

private:
  void put(string s);
};

Minion::Minion() {}

void Minion::get() {
  // This function sends a GET request to our proxy to retrieve the job's json
  // and send it back as a json

  // We don't need to send arguments to our proxy, only the url is important
  cpr::Response r = cpr::Get(cpr::Url{"127.0.0.1:8000"});

  // If the status_code is different from 200, the request didn't go well, so we
  // mustn't process the response.
  if (r.status_code == 200) {

    // First, we transform the json response into a task object
    Task t = decodeJson(r.text);
    // Then we solve the task
    t.work();
    // We transform the task into a json
    string s = t.encodeJson();
    // Finally, we send our result to the proxy
    put(s);
  }
}

void Minion::put(string s) {
  // This function sends a post request to our proxy
  cpr::Post(cpr::Url{"127.0.0.1:8000"}, cpr::Body{s});
}

// Main
// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv) {
  // This line lets Eigen know that it can create several Threads in order to
  // solve several tasks at the same time
  Eigen::setNbThreads(14);

  Minion *m = new Minion();

  while (1) {
    m->get();
  }
}
