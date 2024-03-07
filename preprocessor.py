import re
import pandas as pd

def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = re.findall(pattern,data)
    df = pd.DataFrame({"user_messages": messages, "messages_date": dates})
    df["messages_date"] = pd.to_datetime(df['messages_date'], format="%d/%m/%y, %H:%M - ")
    df.rename(columns={'messages_date': 'date'}, inplace=True)
    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split('([\w\w]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['day_name'] = df['date'].dt.day_name()
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    return df