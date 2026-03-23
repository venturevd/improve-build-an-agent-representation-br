from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Store agents and tasks
agents = {}
tasks = {}

@app.route('/agents', methods=['POST'])
def register_agent():
    data = request.json
    agent_id = data.get('agent_id')
    capabilities = data.get('capabilities', [])

    if agent_id in agents:
        return jsonify({'error': 'Agent already exists'}), 400

    agents[agent_id] = {'capabilities': capabilities}
    return jsonify({'message': 'Agent registered successfully'}), 201

@app.route('/tasks', methods=['POST'])
def submit_task():
    data = request.json
    task_id = data.get('task_id')
    requirements = data.get('requirements', [])

    if task_id in tasks:
        return jsonify({'error': 'Task already exists'}), 400

    tasks[task_id] = {'requirements': requirements}
    return jsonify({'message': 'Task submitted successfully'}), 201

@app.route('/agents/<agent_id>/tasks', methods=['GET'])
def get_matched_tasks(agent_id):
    if agent_id not in agents:
        return jsonify({'error': 'Agent not found'}), 404

    agent_capabilities = set(agents[agent_id]['capabilities'])
    matched_tasks = []

    for task_id, task in tasks.items():
        task_requirements = set(task['requirements'])
        if agent_capabilities.intersection(task_requirements):
            matched_tasks.append(task_id)

    return jsonify({'matched_tasks': matched_tasks}), 200

@app.route('/tasks/<task_id>/agents', methods=['GET'])
def get_matched_agents(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    task_requirements = set(tasks[task_id]['requirements'])
    matched_agents = []

    for agent_id, agent in agents.items():
        agent_capabilities = set(agent['capabilities'])
        if agent_capabilities.intersection(task_requirements):
            matched_agents.append(agent_id)

    return jsonify({'matched_agents': matched_agents}), 200

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'running': True,
        'agents_count': len(agents),
        'tasks_count': len(tasks)
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('BROKER_PORT', 5002))
    app.run(host='127.0.0.1', port=port)