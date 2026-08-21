import json
import os
import sys

# Ensure local backend module import
sys.path.append(os.path.dirname(__file__))

from agent import ChronoCanvasAgent

agent = ChronoCanvasAgent()


def lambda_handler(event, context):
    """
    AWS Lambda entry point for API Gateway HTTP requests and EventBridge scheduled cron events.
    """
    print("Received event:", json.dumps(event))

    # EventBridge Scheduled Event trigger
    if event.get("source") == "aws.events" or "detail-type" in event:
        print("[AWS Lambda] EventBridge trigger fired! Running autonomous agent cycle...")
        result = agent.execute_autonomous_cycle()
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Autonomous cycle executed via EventBridge", "canvas": result})
        }

    # API Gateway HTTP Routing
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
    }

    if http_method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": json.dumps({"status": "ok"})}

    if path.endswith("/canvas/latest") or path == "/":
        canvas = agent.get_latest_canvas()
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(canvas)
        }
    elif path.endswith("/canvas/history"):
        history = agent.get_history()
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(history)
        }
    elif path.endswith("/canvas/generate") and http_method == "POST":
        new_canvas = agent.execute_autonomous_cycle()
        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps(new_canvas)
        }
    else:
        return {
            "statusCode": 404,
            "headers": headers,
            "body": json.dumps({"error": f"Endpoint {path} not found"})
        }
