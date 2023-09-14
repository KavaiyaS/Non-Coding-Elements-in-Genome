# importing necessary libraries
from flask import Flask, render_template, request
import multiprocessing
import time

# creating instance of Flask class
app = Flask(__name__)


# defining a function for comparison of DNA
def compare_dna(healthy_dna, unhealthy_dna, result_queue):
    indices = []  # declare a variable of type list
    process = multiprocessing.current_process()  # storing the current process id in the process variable
    for X in range(0, len(healthy_dna)):  # running a for loop from 0 to length of healthy_dna
        if healthy_dna[X] != unhealthy_dna[
            X]:  # if condition for comparing elements of healthy_dna with unhealthy_dna (the condition becomes true if both the elements do not match)
            indices.append(
                f"{unhealthy_dna[X]} : {X}")  # if the above condition becomes true then the element of unhealthy_dna at 'X'th position and the value of X is appended to the indices variable
    result_queue.put(
        f"{process.name} : {indices}")  # after the loop ends the indices variable and the process name is appended to the result_queue variable
    # print(f"Processed by {process.name}, indices: {indices}")  # Debug print


# creating an app route with 'get' and 'post' methods
@app.route('/', methods=['GET', 'POST'])
# defining a function that is the starting of the logic
def index():
    if request.method == 'POST':  # condition for checking whether request method is 'POST' or not
        healthy_dna = request.form[
            'healthy_dna']  # declaring a variable and initializing it with the user input from the html form input
        unhealthy_dna = request.form[
            'unhealthy_dna']  # declaring a variable and initializing it with the user input from the html form input

        block = 40  # declaring a variable block and assigning static value that defines the number of elements in each block

        healthy_dna_blocks = [healthy_dna[x:x + block] for x in range(0, len(healthy_dna),
                                                                      block)]  # with the help of for loop creating multiple blocks of healthy_dna list and storing it into heallthy_dna_blocks variable
        unhealthy_dna_blocks = [unhealthy_dna[x:x + block] for x in range(0, len(unhealthy_dna),
                                                                          block)]  # with the help of for loop creating multiple blocks of unhealthy_dna list and storing it into unheallthy_dna_blocks variable

        processes = []  # creating an empty list variable

        start = time.time()  # using time function and storing the starting time of the program to start variable

        if len(healthy_dna) != len(unhealthy_dna) or healthy_dna.isdigit() or unhealthy_dna.isdigit() or not healthy_dna.isalpha() or not unhealthy_dna.isalpha():
            return render_template('index.html', error="Error : Please enter the valid input!")
        else:
            result_queue = multiprocessing.Queue()  # creating a queue with the Queue() function

            for h, uh in zip(healthy_dna_blocks,
                             unhealthy_dna_blocks):  # running a for loop for the number of blocks created for both healthy_dna and unhealthy_dna
                p = multiprocessing.Process(target=compare_dna, args=(h, uh,
                                                                      result_queue))  # creating a process for the function compare_dna and assigning that process to the variable p
                p.start()  # starting the process with the help of start() function
                processes.append(p)  # appending the process p to the processes list variable

            for p in processes:  # running a for loop for the number of process in the processes list variable
                p.join()  # joining the output of all the processes with the help of join() function

            result_lists = []  # creating an empty list variable

            # until the result_queue is not empty append the result_queue in the result_lists variable
            while not result_queue.empty():
                result_lists.append(result_queue.get())

            end = time.time()  # using time function and storing the ending time of the program to end variable
            execution_time = end - start  # assigning the difference of end time and start time of the program to the variable execution_time

            # print("Result:", result_lists)  # Debug print

            return render_template('result.html', result=result_lists,
                                   execution_time=execution_time)  # rendering the result.html template and returning result_lists and execution to the template
    else:
        return render_template('index.html')  # else render the index.html template


if __name__ == '__main__':  # while the file is running as a script this condition becomes true
    app.run(debug=True)  # it runs the app on the specific host and port with debugging the codes
