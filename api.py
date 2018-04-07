import requests


api_url = "http://ec2-54-194-150-186.eu-west-1.compute.amazonaws.com:5001"
this_room = "LB04"


def get_lectures(room):
    query = api_url + "/schedules/" + room
    r = requests.get(query).json()
    return r["schedule"]


if __name__ == '__main__':
    lectures = get_lectures(this_room)
    print(len(lectures))
    for lecture in lectures:
        print(lecture["id"], lecture["subject"], lecture["start_time"])