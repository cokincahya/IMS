import requests
import time
import pymysql

db = pymysql.connect("us-cdbr-gcp-east-01.cleardb.net","b4e9053d1cd628","3af726606a78892","gcp_9269858d629149d84891")
cursor = db.cursor()

request_params = {'token': 'LQEg0xpbRFD7U1QzfoB9wKJEqcM4ZmBY0D8mjMrY'}

while True :
    response = requests.get('https://api.groupme.com/v3/groups/50687678/messages', params=request_params)

    if (response.status_code == 200):
        response_messages = response.json()['response']['messages']


        for message in reversed(response_messages):

            pesan = message["text"]

        print(pesan)
        select = "select *from tb_message"
        cursor.execute(select)
        hasil_select = cursor.fetchall()
        db.commit()
        success=0


        for input_message in hasil_select :
            input_message_db = input_message[1]
            if pesan == input_message_db:
                print("data sama")
                success +=1
                to_send = input_message[2]
                print(message['id'])
                sql = "insert into tb_inbox values (null,'%s','%s','%s')" % (message['id'],input_message_db, time.strftime("%Y-%m-%d %H:%M:%S"))
                print(sql)
                cursor.execute(sql)
                db.commit()



                if success >0 :
                    print("Pesan akan dibalas")
                    post_params = {'bot_id': 'f1ccfb72c9c85da16783f8e4f8', 'text': to_send}
                    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
                    request_params['since_id'] = message['id']
                    print(message['id'])
                    sql = "insert into tb_outbox values (null,'%s','%s','%s')" % (message['id'],to_send, time.strftime("%Y-%m-%d %H:%M:%S"))
                    print(sql)
                    cursor.execute(sql)
                    db.commit()



            else :

                print("Pesan tidak akan dibalas")
                print(message['id'])

        time.sleep(1)
