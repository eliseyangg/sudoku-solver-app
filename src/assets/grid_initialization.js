document.addEventListener('DOMContentLoaded', function() {
    // Define the grid options
    const gridOptions = {
        columnDefs: [
            {
                headerName: "Column",
                field: "value",
                cellRenderer: 'CustomCellRenderer',
                cellRendererParams: {
                    // Any additional params
                }
            }
        ],
        components: {
            CustomCellRenderer: CustomCellRenderer
        }
    };

    // Get the grid element and initialize the grid
    const eGridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(eGridDiv, gridOptions);
});