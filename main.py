import pygame
import requests
import tkinter as tk
from tkinter import ttk
import threading

# Default IP
ip = ''
gamepad_thread = None

def sendmsg(message):
    try:
        requests.get('http://' + ip + '/popup.ps3?' + message + '&snd=0')
    except:
        print('no device found')
        ip_label.config(text="Current IP: " + ip + " (Device Not Found)")
        pass

def set_ip():
    global ip
    ip = ip_entry.get()
    update_ip_label()
    update_settings_file()
    sendmsg('Remote Gamepad Connected')

def update_ip_label():
    ip_label.config(text=f"Current IP: {ip}")


def update_settings_file():
    try:
        with open('settings.txt', 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith('ip='):
                    lines[i] = f'ip={ip}\n'
                    break
            else:
                lines.append(f'ip={ip}\n')

        with open('settings.txt', 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        with open('settings.txt', 'w') as file:
            file.write(f'ip={ip}\n')

def read_settings_file():
    global ip
    try:
        with open('settings.txt', 'r') as file:
            for line in file:
                if line.startswith('ip='):
                    ip = line.split('=')[1].strip()
                    sendmsg('Remote Gamepad Connected')
                    break
    except FileNotFoundError:
        pass


# Read IP from settings file
read_settings_file()



def sendbutton(button):
    requests.get('http://' + ip + '/pad.ps3?' + button)

def handle_gamepad():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No gamepad connected.")
        gamepad_label.config(text="No Gamepad Connected")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Gamepad connected: {}".format(joystick.get_name()))
    gamepad_label.config(text="Gamepad connected: {}".format(joystick.get_name()))


    # Initialize variables to store the previous state of the axes
    prev_axes_state = [0.0] * joystick.get_numaxes()

    try:
        while True:
            pygame.event.pump()

            # Check for events (button presses, releases, and analog stick movements)
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    # Handle button presses
                    handle_button_press(event.button)

                elif event.type == pygame.JOYBUTTONUP:
                    # Handle button releases
                    handle_button_release(event.button)

                elif event.type == pygame.JOYAXISMOTION:
                    # Handle analog stick movements
                    handle_joystick_movement(event.axis, event.value, prev_axes_state)

            # Update IP label and Text widget periodically
            root.after(10, update_ip_label)
            update_log_widget()

    except KeyboardInterrupt:
        print("Gamepad thread terminated.")
        sendmsg('Remote Gamepad Disconnected')

    finally:
        pygame.quit()
        sendmsg('Remote Gamepad Disconnected')

def handle_button_press(button):
    # Handle button presses
    if button == 8:
        sendbutton('psbtn')  # PS button
        update_log_widget(f"PS button pressed")
    elif button == 0:
        sendbutton('cross')  # A button
        update_log_widget(f"A button pressed")
    elif button == 1:
        sendbutton('circle')  # B button
        update_log_widget(f"B button pressed")
    elif button == 3:
        sendbutton('triangle')  # Y button
        update_log_widget(f"Y button pressed")
    elif button == 2:
        sendbutton('square')  # X button
        update_log_widget(f"X button pressed")
    elif button == 7:
        sendbutton('start')  # Start button
        update_log_widget(f"Start button pressed")
    elif button == 6:
        sendbutton('select')  # Select button
        update_log_widget(f"Select button pressed")
    elif button == 5:
        sendbutton('r1')  # R1 button
        update_log_widget(f"R1 button pressed")
    elif button == 4:
        sendbutton('r2')  # L1 button
        update_log_widget(f"L1 button pressed")
    else:
        print("Button {} pressed.".format(button))

def handle_button_release(button):
    # Handle button releases
    print("Button {} released.".format(button))
    update_log_widget(f"Button {button} released")

def handle_joystick_movement(axis_id, axis_value, prev_axes_state):
    # Handle analog stick movements
    if abs(axis_value - prev_axes_state[axis_id]) > 0.2:
        print("Axis {} moved to {}.".format(axis_id, axis_value))
        update_log_widget(f"Axis {axis_id} moved to {axis_value}")

        # Left joystick logic
        if axis_id == 0:  # Left joystick X-axis
            if axis_value < -0.8:
                # Left position
                print("Left position")
                sendbutton('analogL_left')
                update_log_widget(f"Left position")
            elif axis_value > 0.8:
                # Right position
                print("Right position")
                sendbutton('analogL_right')
                update_log_widget(f"Right position")

        elif axis_id == 1:  # Left joystick Y-axis
            if axis_value < -0.8:
                # Up position
                print("Up position")
                sendbutton('analogL_up')
                update_log_widget(f"Up position")
            elif axis_value > 0.8:
                # Down position
                print("Down position")
                sendbutton('analogL_down')
                update_log_widget(f"Down position")

        # Update the previous state of the axes
        prev_axes_state[axis_id] = axis_value

def start_gamepad_thread():
    global gamepad_thread
    gamepad_thread = threading.Thread(target=handle_gamepad)
    gamepad_thread.start()

def update_log_widget(text=""):
    if text:
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, text + "\n")
        log_widget.config(state=tk.DISABLED)
        log_widget.see(tk.END)


if __name__ == "__main__":
    # Create Tkinter window
    root = tk.Tk()
    root.title("PS3RemotePad")

    # IP Entry
    ip_label = ttk.Label(root, text=f"Current IP: {ip}")
    ip_label.pack(pady=10)

    gamepad_label = ttk.Label(root, text=f'No Gamepad Detected')
    gamepad_label.pack(pady=5)

    ip_entry = ttk.Entry(root)
    ip_entry.insert(0, ip)
    ip_entry.pack(pady=10)

    set_ip_button = ttk.Button(root, text="Set IP", command=set_ip)
    set_ip_button.pack(pady=10)

    update_ip_label()

    # Text Widget to display button/joystick information
    log_widget = tk.Text(root, height=10, width=40)
    log_widget.pack(pady=10)
    log_widget.config(state=tk.DISABLED)

    # Start the gamepad handling in a separate thread
    start_gamepad_thread()

    # Start the Tkinter main loop
    root.mainloop()
