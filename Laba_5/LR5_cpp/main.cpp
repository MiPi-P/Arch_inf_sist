#include <iostream>
#include "httplib.h"
#include "nlohmann/json.hpp"
#include "foo_engine.h"

using json = nlohmann::json;

int main()
{
#ifdef _WIN32
    system("chcp 65001");
#endif

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

            float left_time = request_json.value("left_time", 0.0f);
            float right_time = request_json.value("right_time", 0.0f);
            float forward_time = request_json.value("forward_time", 0.0f);

            std::cout << "left_time = " << left_time << std::endl;
            std::cout << "right_time = " << right_time << std::endl;
            std::cout << "forward_time = " << forward_time << std::endl;

            if (left_time > 0.0f) {
                std::cout << "TURN LEFT" << std::endl;
                engine.left(left_time);
            }

            if (right_time > 0.0f) {
                std::cout << "TURN RIGHT" << std::endl;
                engine.right(right_time);
            }

            if (forward_time > 0.0f) {
                std::cout << "MOVE FORWARD" << std::endl;
                engine.forward(forward_time);
            }

            if (left_time <= 0.0f && right_time <= 0.0f && forward_time <= 0.0f) {
                engine.stop();
            }

            json response_json;
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

    svr.listen("0.0.0.0", 8080);
    return 0;
}
