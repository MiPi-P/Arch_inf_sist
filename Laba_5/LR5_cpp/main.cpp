#include <iostream>
#include <cmath>
#include "httplib.h"
#include "nlohmann/json.hpp"
#include "foo_engine.h"

using json = nlohmann::json;

int main()
{
    system("chcp 65001");

    FooEngine engine;
    httplib::Server svr;

    svr.Get("/commands", [](const httplib::Request& req, httplib::Response& res) {
        std::cout << "\nGET /commands" << std::endl;
        res.set_content("Server is working", "text/plain");
    });

    svr.Post("/commands", [&engine](const httplib::Request& req, httplib::Response& res) {
        std::string request_body = req.body;

        std::cout << "\nPOST /commands received" << std::endl;
        std::cout << "Raw body: " << request_body << std::endl;

        if (req.get_header_value("Content-Type").find("application/json") == std::string::npos) {
            res.status = 415;
            res.set_content("Unsupported Content-Type. Expected application/json", "text/plain");
            return;
        }

        try {
            json request_json = json::parse(request_body);

            std::string command = request_json.value("command", "none");
            float angle = request_json.value("angle", 0.0f);
            float distance = request_json.value("distance", 0.0f);

            std::cout << "command = " << command << std::endl;
            std::cout << "angle = " << angle << std::endl;
            std::cout << "distance = " << distance << std::endl;

            if (command == "move") {
                if (angle > 10.0f) {
                    std::cout << "TURN RIGHT" << std::endl;
                    engine.right(angle);
                }
                else if (angle < -10.0f) {
                    std::cout << "TURN LEFT" << std::endl;
                    engine.left(std::abs(angle));
                }
                else {
                    std::cout << "NO ROTATION NEEDED" << std::endl;
                }

                if (distance > 5.0f) {
                    std::cout << "MOVE FORWARD" << std::endl;
                    engine.forward(distance);
                }
                else {
                    std::cout << "TARGET IS CLOSE" << std::endl;
                    engine.stop();
                }
            }
            else {
                std::cout << "Unknown command" << std::endl;
            }

            json response_json;
            response_json["message"] = "Command received successfully";
            response_json["received_command"] = command;
            response_json["received_angle"] = angle;
            response_json["received_distance"] = distance;
            response_json["status"] = "success";

            res.set_content(response_json.dump(), "application/json");
            res.status = 200;
        }
        catch (const json::parse_error& e) {
            res.status = 400;
            res.set_content("Invalid JSON format: " + std::string(e.what()), "text/plain");
        }
    });

    std::cout << "Server listening on http://localhost:8080" << std::endl;
    std::cout << "Try: curl -X POST -H \"Content-Type: application/json\" -d '{\"command\": \"move\", \"angle\": -90, \"distance\": 27,}' http://localhost:8080/commands" << std::endl;

    svr.listen("0.0.0.0", 8080);
    return 0;
}