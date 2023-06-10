from const import Constants
from flask import Flask, render_template, request
from utils import fetch_data, generategraph
from dominant_phone import Phone, get_dominant_phones

app = Flask(__name__)


@app.route("/")
def home():
    """
    Render the home page.

    Returns:
        A rendered HTML template with the graph embedded.

    Raises:
        Exception: If any error occurs during the execution.
    """
    try:
        html_string = generategraph(x_axis_data=[], y_axis_data=[], names=[],x_axis="processor",y_axis="processor")

        return render_template(Constants.INDEX_TEMPLATES, graph=html_string)
    except Exception as ex:
        return render_template(Constants.ERROR_TEMPLATES, error_message=ex)

@app.route("/showphonelist")
def show_phone_list():
    """
    List all the available Phone
    """
    phone_details = fetch_data(query="select processor,cost,ram,name from phone_info")
    return render_template("show_phones.html",phone_details=phone_details)

@app.route("/generategraph", methods=["POST"])
def generate_graph():
    """
    Generate and display a graph based on the selected x-axis and y-axis.

    Returns a rendered HTML template with the embedded graph.

    Raises:
        Exception: If any error occurs during the execution.
    """
    try:
        x_axis = request.form.get(Constants.X_AXIS)
        y_axis = request.form.get(Constants.Y_AXIS)
        rows = fetch_data(
            query=f"select {x_axis},{y_axis},name from phone_info order by {x_axis} ASC"
        )
        x_axis_data = []
        y_axis_data = []
        names = []
        for row in rows:
            x_axis_data.append(row[0])
            y_axis_data.append(row[1])
            names.append(row[2])
        html_string = generategraph(x_axis_data=x_axis_data, y_axis_data=y_axis_data, names=names, x_axis = x_axis, y_axis = y_axis)
        return render_template(Constants.INDEX_TEMPLATES, graph=html_string,names = names)
    except Exception as ex:
        return render_template(Constants.ERROR_TEMPLATES, error_message=ex)


@app.route("/dominantphone", methods=["POST"])
def find_dominant_phone():
    """
    Retrieve data for non-dominant phones from the database and generate a graph based on the selected axes.

    Returns:
        str: HTML string of the generated graph embedded in the template.

    Raises:
        Exception: If any error occurs during the execution.
    """
    try:
        query = "select processor,cost,ram,name from phone_info"
        phone_data = fetch_data(query=query)
        #changing the type in Phone type
        phones = [
            Phone(cost=cost, name=name, processor=processor, ram=ram)
            for processor, cost, ram, name in phone_data
        ]

        dominant_phones = get_dominant_phones(phones=phones)
        
        rows = [
            (
                dominant_phone.processor,
                dominant_phone.cost,
                dominant_phone.ram,
                dominant_phone.name,
            )
            for dominant_phone in dominant_phones
        ]
        x_axis = request.form.get(Constants.X_AXIS)
        y_axis = request.form.get(Constants.Y_AXIS)
        x_axis_data = []
        y_axis_data = []
        names = []
        for row in rows:
            x_axis_data.append(row[Constants.AXIS_MAP.get(x_axis)])
            y_axis_data.append(row[Constants.AXIS_MAP.get(y_axis)])
            names.append(row[Constants.AXIS_MAP.get("name")])
        html_string = generategraph(x_axis_data=x_axis_data, y_axis_data=y_axis_data, names=names,x_axis=x_axis,y_axis=y_axis)
        return render_template(Constants.INDEX_TEMPLATES, graph=html_string,names = names)
    except Exception as ex:
        return render_template(Constants.ERROR_TEMPLATES, error_message=ex)


if __name__ == "__main__":
    app.run(debug=True)
