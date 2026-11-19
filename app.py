from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")


def trace_find_duplicate(nums):
    """Run Floyd's cycle detection and record every step."""
    steps = []
    slow = fast = 0
    steps.append(dict(phase=1, slow=slow, fast=fast, slow2=None,
                      msg="Start: slow and fast both at index 0."))

    # Phase 1: find a meeting point inside the cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        met = slow == fast
        steps.append(dict(
            phase=1, slow=slow, fast=fast, slow2=None,
            msg=f"slow moves 1 step, fast moves 2 steps."
                + (f" They meet at index {slow}, inside the cycle." if met else "")))
        if met:
            break

    # Phase 2: find the cycle entrance (the duplicate)
    slow2 = 0
    steps.append(dict(phase=2, slow=slow, fast=None, slow2=slow2,
                      msg=f"Restart a second pointer at 0. The first stays at {slow}. Both now move 1 step."))
    while slow2 != slow:
        slow2 = nums[slow2]
        slow = nums[slow]
        steps.append(dict(
            phase=2, slow=slow, fast=None, slow2=slow2,
            msg="Both pointers move 1 step."
                + (f" They meet at {slow}: that is the duplicate." if slow2 == slow else "")))

    return steps, slow


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/trace")
def api_trace():
    raw = request.args.get("nums", "1,3,4,2,2")
    try:
        nums = [int(x) for x in raw.replace(" ", "").split(",") if x != ""]
    except ValueError:
        return jsonify(error="nums must be comma-separated integers"), 400

    n = len(nums) - 1
    if n < 1:
        return jsonify(error="Need at least 2 numbers."), 400
    if any(v < 1 or v > n for v in nums):
        return jsonify(error=f"With {len(nums)} numbers, every value must be between 1 and {n}."), 400

    steps, duplicate = trace_find_duplicate(nums)
    return jsonify(nums=nums, steps=steps, duplicate=duplicate)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
