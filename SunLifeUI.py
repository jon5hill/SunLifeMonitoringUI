import time
import tkinter as tk
import webbrowser
import datetime
import json
import httplib2

window = tk.Tk()


def callback(url):
    webbrowser.open_new(url)


def add_header(frame_header):
    header = tk.Label(master=frame_header, text="Maxwell Health / Sun Life Monitoring", font=("Arial", 40))
    status_message = tk.Label(master=frame_header, text="", font=("Arial", 10))
    header.pack()
    status_message.pack()
    frame_header.pack()


def update_header(frame_header, counter):
    print(str(counter) + "seconds")
    status_message = frame_header.winfo_children()[1]
    status_message.destroy()
    message = str(counter) + " seconds until next http calls"
    status_message = tk.Label(master=frame_header, text=message, font=("Arial", 10))
    status_message.pack()
    frame_header.pack()


def add_endpoints(frame_header, title):
    header = tk.Label(master=frame_header, text=title, font=("Arial", 25))
    status_message1 = tk.Label(master=frame_header, text="URL:", font=("Arial", 15))
    status_message2 = tk.Label(master=frame_header, text="Status Code:", font=("Arial", 15))
    status_message3 = tk.Label(master=frame_header, text="Duration:   ", font=("Arial", 15))
    status_message4 = tk.Label(master=frame_header, text="Date:       ", font=("Arial", 15))
    header.pack()
    status_message1.pack()
    status_message2.pack()
    status_message3.pack()
    status_message4.pack()
    frame_header.pack()


def display_message(message, frame_header):
    status_message1 = frame_header.winfo_children()[1]
    status_message2 = frame_header.winfo_children()[2]
    status_message3 = frame_header.winfo_children()[3]
    status_message4 = frame_header.winfo_children()[4]
    status_message1.destroy()
    status_message2.destroy()
    status_message3.destroy()
    status_message4.destroy()
    message1 = "URL:  " + str(message["url"])
    message2 = "Status Code:  " + str(message["statusCode"])
    message3 = "Duration:  " + str(message["duration"])
    date = datetime.datetime.fromtimestamp(message["date"]).astimezone()
    message4 = "Date:  " + str(date)
    status_message1 = tk.Label(master=frame_header, text=message1, font=("Arial", 15))
    status_message2 = tk.Label(master=frame_header, text=message2, font=("Arial", 15))
    status_message3 = tk.Label(master=frame_header, text=message3, font=("Arial", 15))
    status_message4 = tk.Label(master=frame_header, text=message4, font=("Arial", 15))
    status_message1.pack()
    status_message2.pack()
    status_message3.pack()
    status_message4.pack()
    frame_header.pack()


def http_request(url, frame_header):
    print('Calling API with URL: {0} '.format(url))
    try:
        response, content = httplib2.Http().request(url)
        content_json = json.loads(content)
        display_message(content_json, frame_header)
        print(content_json["url"])
        print(content_json["statusCode"])
        print(content_json["duration"])
        print(content_json["date"])
    except:
        error_json = {"url":url, "statusCode":"500", "duration":0, "date":int(time.time())}
        display_message(error_json, frame_header)


def http_request_all(url, frame_header3, frame_header4):
    print('Calling API with URL: {0} '.format(url))
    try:
        response, content = httplib2.Http().request(url)
        content_json = json.loads(content)
        if content_json[0]["url"] == "https://www.amazon.com":
            display_message(content_json[1], frame_header3)
            display_message(content_json[0], frame_header4)
        else:
            display_message(content_json[0], frame_header3)
            display_message(content_json[1], frame_header4)
        for i in [0, 1]:
            print(content_json[i]["url"])
            print(content_json[i]["statusCode"])
            print(content_json[i]["duration"])
            print(content_json[i]["date"])
    except:
        error_json = {"url":url, "statusCode":"500", "duration":0, "date":int(time.time())}
        display_message(error_json, frame_header3)
        display_message(error_json, frame_header4)


def repeat_calls(frame_header, frame_header1, frame_header2, frame_header3, frame_header4):
    counter = 59 - (round(time.time()) % 60)
    update_header(frame_header, counter)
    if counter == 0:
        http_request("http://localhost/v1/google-status", frame_header1)
        http_request("http://localhost/v1/amazon-status", frame_header2)
        http_request_all("http://localhost/v1/all-status", frame_header3, frame_header4)
    window.after(1000, repeat_calls, frame_header, frame_header1, frame_header2, frame_header3, frame_header4)


def main():
    frame_header = tk.Frame(master=window, relief=tk.RIDGE, height=10, borderwidth=5)
    add_header(frame_header)
    frame_header1 = tk.Frame(master=window, relief=tk.RIDGE, height=10, borderwidth=5)
    add_endpoints(frame_header1, "GOOGLE")
    frame_header2 = tk.Frame(master=window, relief=tk.RIDGE, height=10, borderwidth=5)
    add_endpoints(frame_header2, "AMAZON")
    frame_header3 = tk.Frame(master=window, relief=tk.RIDGE, height=10, borderwidth=5)
    add_endpoints(frame_header3, "ALL - GOOGLE")
    frame_header4 = tk.Frame(master=window, relief=tk.RIDGE, height=10, borderwidth=5)
    add_endpoints(frame_header4, "ALL - AMAZON")
    http_request("http://localhost/v1/google-status", frame_header1)
    http_request("http://localhost/v1/amazon-status", frame_header2)
    http_request_all("http://localhost/v1/all-status", frame_header3, frame_header4)
    window.after(0, repeat_calls(frame_header, frame_header1, frame_header2, frame_header3, frame_header4))
    window.mainloop()


if __name__ == "__main__":
    main()
