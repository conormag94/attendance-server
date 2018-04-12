import requests


api_url = "http://ec2-54-194-150-186.eu-west-1.compute.amazonaws.com:5001"
this_room = "LB04"


def get_test_schedule():
    query = api_url + '/test'
    r = requests.get(query).json()
    return r['schedule']


def get_lectures(room):
    query = api_url + "/schedules/" + room
    r = requests.get(query).json()
    return r["schedule"]


def upload_attendance(students, lecture_id):
    query = '{0}/lectures/{1}'.format(api_url, lecture_id)
    r = requests.post(query, json={'student_numbers': students}).json()
    return r


if __name__ == '__main__':
    # lectures = get_lectures(this_room)
    lectures = get_test_schedule()
    print(len(lectures))
    for lecture in lectures:
        print(lecture["id"], lecture["subject"], lecture["start_time"])