document.addEventListener('DOMContentLoaded', function () {

    const filterButton = document.getElementById('filter-button');

    const nameFilter = document.getElementById('name-filter');

    const statusFilter = document.getElementById('status-filter');

    const dateFrom = document.getElementById('date-from');

    const dateTo = document.getElementById('date-to');

    const reportTableBody = document.getElementById('report-table-body');


    filterButton.addEventListener('click', function () {

        const nameValue = nameFilter.value;

        const statusValue =statusFilter.value;

        const fromDate = new Date(dateFrom.value);

        const toDate = new Date(dateTo.value);

        const rows = reportTableBody.getElementsByTagName('tr');


        for (let row of rows) {

            const nameCell = row.cells[0].textContent;

            const statusCell = row.cells[6].textContent;

            const dateCell = new Date(row.cells[5].textContent);


            const nameMatch = nameValue ? nameCell === nameValue : true;

            const statusMatch = statusValue ? statusCell === statusValue : true;

            const dateMatch = (isNaN(fromDate) || dateCell >= fromDate) && (isNaN(toDate) || dateCell <= toDate);


            if (nameMatch && statusMatch && dateMatch) {

                row.style.display = '';

            } else {

                row.style.display = 'none';

            }

        }

    });

});