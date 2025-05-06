from flask import Flask, request, jsonify
import kociemba
import pytwisty

app = Flask(__name__)

@app.route('/solve', methods=['GET'])
def solve_cube():
    cube_string = request.args.get('cube')

    if not cube_string:
        return jsonify({'error': 'No cube string provided'}), 400

    cube_string = cube_string.upper()
    length = len(cube_string)

    try:
        if length == 24:
            # 2x2x2: 6 faces × 4 stickers = 24
            if not _validate_colors(cube_string, 4):
                return jsonify({'error': '2x2x2 must have 4 of each of 6 colors'}), 400

            solution = pytwisty.solve222(cube_string)
            return jsonify({'type': '2x2x2', 'solution': solution})

        elif length == 54:
            # 3x3x3: 6 faces × 9 stickers = 54
            if not _validate_colors(cube_string, 9):
                return jsonify({'error': '3x3x3 must have 9 of each of 6 colors'}), 400

            solution = kociemba.solve(cube_string)
            return jsonify({'type': '3x3x3', 'solution': solution})

        else:
            return jsonify({'error': 'Cube string must be 24 (2x2x2) or 54 (3x3x3) characters'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def _validate_colors(cube, expected_count):
    """Check if cube string has 6 colors, each appearing expected_count times."""
    from collections import Counter
    color_counts = Counter(cube)
    return len(color_counts) == 6 and all(count == expected_count for count in color_counts.values())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
