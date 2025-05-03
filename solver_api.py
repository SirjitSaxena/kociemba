from flask import Flask, request, jsonify
import kociemba

app = Flask(__name__)

@app.route('/solve', methods=['GET'])
def solve_cube():
    cube_string = request.args.get('cube')
    
    if not cube_string:
        return jsonify({'error': 'No cube string provided'}), 400

    try:
        # Solve the cube
        solution = kociemba.solve(cube_string.upper())
        return jsonify({'solution': solution})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
