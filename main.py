import state_machine
import image_cycler

if __name__ == "__main__":
    try:
        state_machine.main()
    except Exception as e:
        image_cycler.displays["error"].display_current_image()
        print("Error detected:", e)
