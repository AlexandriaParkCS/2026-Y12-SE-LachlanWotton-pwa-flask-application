async function genTable() 
{
    const tasks = [];
    
    const data = await fetchData('*');  
    console.log(data)
    console.log(typeof data)

    if(data != null)
    {
    var tableBody = document.getElementById("tableBody");
    
    data.forEach(task => {
        var newRow = tableBody.insertRow();

        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3);
        var cell5 = newRow.insertCell(4);
        var cell6 = newRow.insertCell(5);
        var cell7 = newRow.insertCell(6);

        var date = new Date(task.due_date);
        var score = task.earned_marks + "/" + task.total_marks;
        var percent = task.Percent + "%";

        cell1.innerHTML = task.Name;
        cell2.innerHTML = date.toLocaleDateString();
        cell3.innerHTML = task.course;
        cell4.innerHTML = task.type;
        cell5.innerHTML = task.format;
        cell6.innerHTML = score;
        cell7.innerHTML = percent;
    });
    }
}

async function fetchData(query)
{
    var fetchText = "http://127.0.0.1:5000/return_data/" + query;
    var data = await fetch(fetchText).then(response =>{
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log('valid response');
        return response;
    });
    var response = await data.json();
    console.log(response);
    return response;
}

function parseDate(string, separator)
{
    const parts = string.split(separator)
    const dateObj = new Date(parts[2], parts[1] - 1, parts[0]);
    return dateObj
}

function tableClick(columnId = '*')
{
    // Get a reference to the table
    const table = document.getElementById('tableBody');
    const popup = document.getElementById('scoreInput');

    // Add a click event listener to the table
    table.addEventListener('click', function(event) {
        // `event.target` is the specific element clicked (e.g., the <td> or content inside it)
        let clickedCell = event.target;

        // Ensure we are dealing with a TD element (in case content inside the TD was clicked)
        if (clickedCell.tagName.toLowerCase() !== 'td') {
            clickedCell = clickedCell.closest('td');
        }

        // Check if the clicked cell exists and belongs to the specified column index (0 for the first column)
        // `cellIndex` starts at 0, so the first column is 0.
        switch(columnId){
            case columnId = '*':
                if(clickedCell)
                {
                    row = clickedCell.parentNode;
                    taskName = row.cells[0];
                    
                }
            default:
                if (clickedCell && clickedCell.cellIndex === columnId) 
                {
                    
                }
        }
    });
}

genTable();
