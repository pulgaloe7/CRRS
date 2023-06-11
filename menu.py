from tkinter import *
import requests
import json
import pandas as pd
#

URL_TOURNAMENTS = 'https://api.clashroyale.com/v1/tournaments'
URL_BATTLELOG = 'https://api.clashroyale.com/v1/players/%2382UUGL0YC/battlelog'
URL_PLAYER = 'https://api.clashroyale.com/v1/players/%2382UUGL0YC'


headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExMTgyZGZjLTQwNmQtNDA2Zi1hMTg0LTI0OTE1ODdjYWU1OSIsImlhdCI6MTY4NTQxMjEyNCwic3ViIjoiZGV2ZWxvcGVyLzA0NGExZjVjLTQwYWItOTYyYS1lNzBhLTI3ZWU5Yjk2YjZhMiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODkuMjE2LjE0OS4xIl0sInR5cGUiOiJjbGllbnQifV19.LDsYdt59EmI-dBAC3p3jOT7BF3gFI-S-G_Re_xyCQiZ3eDTc3IM3Ri1XexHLHHBk0Jr-PC7r2fVWNmIS3TBuiw'
}

root = Tk()
root.title("Clash Royale Recommendation System")

e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

def get_all_tournaments():
    response = requests.get(url=URL_TOURNAMENTS + '?name=' + e.get(), headers=headers)
    print("Tournament status code: " + str(response.status_code))

    if response.status_code == 200:
        items_obj = json.loads(response.text)
        items_list = items_obj.get('items')

        result_window = Toplevel(root)
        result_window.title("Results")

        text_widget = Text(result_window, width=100, height=100)
        text_widget.pack()

        for item in items_list:
            result = (
                'Name: ' + item['name'] +
                '\nStatus: ' + item['status'] +
                '\nTag: ' + item['tag'] +
                '\nMax Capacity: ' + str(item['maxCapacity']) +
                '\nCapacity: ' + str(item['capacity']) +
                '\n======================\n'
            )
            text_widget.insert(END, result)

def get_player_battle_log():
    BATTLELOG = URL_BATTLELOG.replace('82UUGL0YC', e.get())
    response = requests.get(url=BATTLELOG, headers=headers)
    print("Player Battle Log Status code: " + str(response.status_code))

    if response.status_code == 200:
        battle_logs = response.json()
        cards_vec = []

        for log in battle_logs:
            team = log['team']
            for card in team[0]['cards']:
                cards_vec.append(card['name'])

        cartas_vec = pd.Series(cards_vec)

        max_card = cartas_vec.value_counts().idxmax()
        min_card = cartas_vec.value_counts().idxmin()

        result_window = Toplevel(root)
        result_window.title("Battle Log Results")

        text_widget = Text(result_window, width=100, height=100)
        text_widget.pack()

        result = (
            "En los últimos 25 juegos la carta más repetida es: " + max_card +
            "\nEn los últimos 25 juegos la carta menos repetida es: " + min_card +
            "\n\nRecomendaciones de mazo:"
        )
        text_widget.insert(END, result)

        recommendation_count = 0

        for log in battle_logs:
            team = log['team']
            crowns = team[0]['crowns']
            opponent = log['opponent']
            crowns_opponent = opponent[0]['crowns']

            player_cards = [card['name'] for card in team[0]['cards']]

            if max_card in player_cards and crowns_opponent > crowns:
                recommendation = "\n\nTe recomiendo usar el siguiente mazo:\n"
                for cardop in opponent[0]['cards']:
                    recommendation += '- ' + cardop['name'] + '\n'
                
                text_widget.insert(END, recommendation)
                recommendation_count += 1

                if recommendation_count == 3:
                    break

    else:
        print("No se pudo obtener el registro de batallas del jugador.")

button_GetPBattleLog = Button(root, text="Get Battle Log", padx=40, pady=20, command=get_player_battle_log)
button_GetPBattleLog.grid(row=1, column=0, columnspan=3)


button_GetPlayer = Button(root, text="Tournaments!", padx=40, pady=20, command=get_all_tournaments)
button_GetPlayer.grid(row=2, column=0, columnspan=3)

root.mainloop()
