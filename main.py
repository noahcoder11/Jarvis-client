from JarvisClient import JarvisClient

jarvis_client = JarvisClient("http://localhost:5000")

def jarvis_run_cycle():
    jarvis_client.run_cycle()

while True:
    jarvis_client.main(jarvis_run_cycle)