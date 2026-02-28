import state_machine
import data_parsers

station_data = {
    "staNm": ["Racine"],
    "staId": [40470],
    "staData": []
}

data_parsers.get_and_parse_data(station_data)

if __name__ == "__main__":
    try:
        state_machine.main()
    except Exception as e:
        print("Error detected:", e)
