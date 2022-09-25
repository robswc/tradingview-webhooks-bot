$(document).ready(function () {
    function getLogData() {
        $.ajax({
            url: '/logs',
            type: 'GET',
            success: function (data) {
                data.reverse()
                createLogs(data.splice(0, 10));
            },
            error: function (error) {
                console.log(error)
                return []
            }
        })
    }

    function createLogs(logData) {
        // get log container
        let logContainer = document.getElementById('logContainer');
        // clear log container
        logContainer.innerHTML = '';
        // create div for each log
        logData.forEach(log => {

            // create div for log parent
            let parent = document.createElement('div');
            parent.classList.add('fw-bolder');
            parent.classList.add('mb-2');
            parent.classList.add('me-2');
            parent.classList.add('text-primary');
            parent.innerHTML = log.parent;

            let logHeader = document.createElement('div');
            // add classes to log div
            logHeader.classList.add('d-flex');
            logHeader.classList.add('justify-content-between');
            logHeader.innerHTML = parent.outerHTML + log.event_data;

            let logEnder = document.createElement('div');
            logEnder.classList.add('text-muted');
            logEnder.classList.add('mono');
            logEnder.innerHTML = new Date(log.event_time).toLocaleString();

            let logDiv = document.createElement('div');
            // add classes to log div
            logDiv.classList.add('d-flex');
            logDiv.classList.add('justify-content-between');
            logDiv.classList.add('w-100');
            logDiv.innerHTML = logHeader.outerHTML + logEnder.outerHTML;
            logContainer.appendChild(logDiv);
        })
    }

    getLogData();
    setInterval(function () {
        getLogData()
    }, 10000);
});