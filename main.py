import pygame
import requests

ip = '192.168.1.14' #your consoles ip address

def sendmsg(message):
    requests.get('http://' + ip + '/popup.ps3?' + message + '&snd=0')

sendmsg('Remote Gamepad Connected')

def sendbutton(button):
    requests.get('http://' + ip + '/pad.ps3?' + button)

def main():
    pygame.init()

    pygame.joystick.init()


    if pygame.joystick.get_count() == 0:
        print("No gamepad connected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Gamepad connected: {}".format(joystick.get_name()))

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

    except KeyboardInterrupt:
        print("Application terminated.")
        sendmsg('Remote Gamepad Disconnected')

    finally:
        pygame.quit()
        sendmsg('Remote Gamepad Disconnected')

def handle_button_press(button):
    # Handle button presses
    if button == 8:
        sendbutton('psbtn')  # PS button
    elif button == 0:
        sendbutton('cross')  # A button
    elif button == 1:
        sendbutton('circle')  # B button
    elif button == 3:
        sendbutton('triangle')  # Y button
    elif button == 2:
        sendbutton('square')  # X button
    elif button == 7:
        sendbutton('start')  # Start button
    elif button == 6:
        sendbutton('select')  # Select button
    elif button == 5:
        sendbutton('r1')  # R1 button
    elif button == 4:
        sendbutton('r2')  # L1 button
    else:
        print("Button {} pressed.".format(button))

def handle_button_release(button):
    # Handle button releases
    print("Button {} released.".format(button))

def handle_joystick_movement(axis_id, axis_value, prev_axes_state):
    # Handle analog stick movements
    if abs(axis_value - prev_axes_state[axis_id]) > 0.2:
        print("Axis {} moved to {}.".format(axis_id, axis_value))

        # Left joystick logic
        if axis_id == 0:  # Left joystick X-axis
            if axis_value < -0.8:
                # Left position
                print("Left position")
                sendbutton('analogL_left')
            elif axis_value > 0.8:
                # Right position
                print("Right position")
                sendbutton('analogL_right')

        elif axis_id == 1:  # Left joystick Y-axis
            if axis_value < -0.8:
                # Up position
                print("Up position")
                sendbutton('analogL_up')
            elif axis_value > 0.8:
                # Down position
                print("Down position")
                sendbutton('analogL_down')

        # Update the previous state of the axes
        prev_axes_state[axis_id] = axis_value

if __name__ == "__main__":
    main()
