from flask import Flask, request, render_template, redirect
import csv

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Validate required fields: email, subject, and body
        if not all(field in data and data[field] for field in ('Email', 'subject', 'body')):
            # Display error message and redirect to contact.html
            error_message = "Please fill in all required fields: Email, Subject, and Body."
            return render_template('contact.html', error_message=error_message)

        email = data['Email']
        subject = data['subject']
        body = data['body']

        write_to_csv(email, subject, body)
        return redirect('/thank you.html')  # Assuming thank you.html exists
    else:
        return "This route expects a POST request"

def write_to_csv(email, subject, body):
    with open('database.csv', 'a', newline='') as database:
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, body])

@app.route('/<page_name>')
def page(page_name):
    try:
        return render_template(page_name)
    except:
        return "Page not found", 404

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('/assets/favicon.ico')

if __name__ == "__main__":
    app.run(debug=True)