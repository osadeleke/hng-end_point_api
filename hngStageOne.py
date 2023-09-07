from flask import Flask, request, jsonify
import datetime

hngStageOne = Flask(__name__)

@hngStageOne.route('/api', methods=['GET'])
def my_endpoint_function():
    slack_name = request.args.get('slack_name')
    track = request.args.get('track')

    current_day = datetime.datetime.utcnow().strftime('%A')
    utc_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    github_repo_url = "https://github.com/osadeleke/"
    github_file_url = "https://github.com/osadeleke/hng-end_point_api/blob/master/hngStageOne.py"

    response = {
            "slack_name": slack_name,
            "current_day": current_day,
            "utc_time": utc_time,
            "track": track,
            "github_file_url": github_file_url,
            "github_repo_url": github_repo_url,
            "status_code": 200
    }
    return jsonify(response)

if __name__ == '__main__':
    hngStageOne.run()
