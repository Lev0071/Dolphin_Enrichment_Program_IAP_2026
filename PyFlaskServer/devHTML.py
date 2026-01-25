#Line 600 on integratev1.py is the beginning of the flask code. This file is basically used to develop the app routing and html file and is then copy and pasted into the server code.
import flask
import time
'''
This file serves as the main HTML/CSS client side development file

Changes are made here first then synced into the main server code file.
'''
server_data={'buttons':[0,0,0,0,0,0,0,0,0],
			 'button_states':[0,0,0,0,0,0,0,0,0],
			 'logging_message':"",
			 "hose_override":False,
			 "game_status":False,
			 "game_time":8,
			 "hose_time":8,
			 "coop_button_time":5,
			 "coop_game_status":False}

app = flask.Flask(__name__)

def reset_arduino():
	print("Reset arduino called")
def start_random_game():
	global server_data
	server_data['logging_message']="Start random game"
	server_data['game_status']=True

def stop_random_game():
	global server_data
	server_data['logging_message']="Stop random game"
	server_data['game_status']=False
def perform_scan():
	print("perform scan called")
	

@app.route('/')
def index():
    global server_data
    return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/reset_buttons_pressed')
def reset_buttons_flask_route():
	global server_data
	#This is just a button that restarts the arduinos, should relab
	reset_arduino()
	server_data['logging_message']="Reset Buttons button pushed"
	return flask.render_template('devhtml.html',serverdata=server_data)
@app.route('/shutdown_system')
def shutdown_system_flask_route():
	global server_data
	#Write code for shutting things down.
	server_data['logging_message']="Shutdown System button pushed"
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/reboot_rasberry_pi')
def reboot_rasberry_pi_flask_route():
	global server_data
	#Write code for shutting down the pi.
	server_data['logging_message']="Reboot resberry pi button pushed"

	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/restart_program')
def restart_program_flask_route():
	#Write code for restarting the program.
	global server_data
	server_data['logging_message']="Restart program button pushed"

	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/change_hose_time/',methods=['POST'])
def change_hose_time_flask_route():
	global server_data	
	global SolSec
	new_hose_time=flask.request.form.get('hose_time')
	server_data['hose_time']=new_hose_time
	server_data['logging_message']="New hose time is " + str(new_hose_time) + " Seconds"
	SolSec=new_hose_time
	return flask.render_template('devhtml.html',serverdata=server_data)


@app.route('/set_new_interval_time/<int:new_interval_time>',methods=['POST'])
def set_new_interval_time(new_interval_time):
	global server_data
	global IntervalTime
	IntervalTime=new_interval_time
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/start_random_game')
def start_random_game_flask_route():
	global server_data
	start_random_game()
	print("AHHH,AHHH)")
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/stop_random_game')
def stop_random_game_flask_route():
	global server_data
	server_data['logging_message']="Stop random game"
	stop_random_game()
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/scan_button_pressed', methods=['GET'])
def scan_button_pressed_flask():
	global server_data	
	perform_scan()
	return flask.render_template('devhtml.html',serverdata=server_data)
@app.route('/button_click/<int:button_id>',methods=['POST'])
def button_click_server(button_id):
	global server_data
	if server_data['button_states'][button_id]==1:
		server_data['button_states'][button_id]=0
	else:
		server_data['button_states'][button_id]=1
	server_data['logging_message']="button "+str(button_id+1) + " Pressed. Button is now " + str(bool(server_data['button_states'][button_id]))

	return flask.render_template('devhtml.html',serverdata=server_data)
@app.route('/toggle_override',methods=['POST'])
def toggle_override():
	global server_data
	server_data['logging_message']="Hose override toggeled" 
	server_data['hose_override']=not server_data['hose_override']
	return flask.render_template('devhtml.html',serverdata=server_data)
	
@app.route('/set_game_time',methods=['POST'])
def set_game_time():
	global server_data
	game_time=flask.request.form.get('game_time')
	print(game_time)
	server_data['game_time']=game_time
	server_data['logging_message']="Set game_time to " + str(game_time)
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/change_coop_button_time',methods=['POST'])
def change_coop_button_time():
	global server_data	
	#global SolSec
	new_button_time=flask.request.form.get('coop_button_time')
	server_data['coop_button_time']=new_button_time
	server_data['logging_message']="New co-op button time time is " + str(new_button_time) + " Seconds"
	#SolSec=new_button_time
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/start_coop_game')
def start_coop_game():
	global server_data
	server_data['logging_message']="Start coop random game"
	server_data['coop_game_status']=True
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/stop_coop_game')
def stop_coop_game():
	global server_data
	server_data['logging_message']="Stop coop random game"
	server_data['coop_game_status']=False
	return flask.render_template('devhtml.html',serverdata=server_data)

@app.route('/stream')
def stream_logging_data():
    def generate():
        while True:
            time.sleep(1)

            yield f"data: Latest logging message: " + server_data['logging_message'] +  "\n\n"
    return flask.Response(generate(),mimetype="text/event-stream")

@app.route('/update_button_colour/<button_id>', methods=['POST','GET'])
def update_colour(button_id):
	button_number=int(button_id[len(button_id)-1])-1
	if server_data['button_states'][button_number]==1:
		return flask.jsonify(new_color="green")
	else:
		return flask.jsonify(new_color="red")




@app.route('/start_simulate_press/<button_id>', methods=['POST'])
def start_stimulating_button(button_id):
    global button_status
	
    button_number=int(button_id[len(button_id)-1])-1
    server_data['button_states'][button_number]=1
    '''
	if server_data['button_states'][button_number]==1:
        server_data['button_states'][button_number]=0
    else:
        server_data['button_states'][button_number]=1
'''
    
    print("Button status updated to:")  # For debugging purposes
    return "Button status is now: "

@app.route('/stop_simulate_press/<button_id>', methods=['POST'])
def stop_simulating_button(button_id):
    global button_status
	
    button_number=int(button_id[len(button_id)-1])-1
    server_data['button_states'][button_number]=0
	#perform_scan()
    '''
	if server_data['button_states'][button_number]==1:
        server_data['button_states'][button_number]=0
    else:
        server_data['button_states'][button_number]=1
'''
    
    print("Button status updated to:")  # For debugging purposes
    return "Button status is now: "


if __name__ == '__main__':
	#Initalise the flask server code.
    app.run(debug=True, host='0.0.0.0', port=8080)
