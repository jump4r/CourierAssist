class JsCalendar {
    constructor() {
        this.monthNames = [
                        "January", "Februrary", "March",
                        "April", "May", "June", "July", "August",
                        "September", "October", "November", "December"
                    ];
        this.numDays = {
            "January": 31,
            "Februrary": 28,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        };
        this.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        
        this.selected = new Date();
        this.selectedNode = null;

        this.monthNode = document.querySelector('.calendar-month');
        this.yearNode = document.querySelector('.calendar-year');

        // Displayed in a monthly format, so we need a current month/year var
        this.activeMonth = this.selected.getMonth();
        this.activeYear = this.selected.getFullYear();

        this.constructCalendar(this.activeMonth, this.activeYear, true);
    }

    constructCalendar(month, year, init=false) {
        let first = new Date(year, month, 1);
        let dayOfWeek = first.getDay();

        let date_list = document.querySelectorAll(".calendar-date");
        let checkForSelectedNode = (this.activeMonth == this.selected.getMonth() && this.activeYear == this.selected.getFullYear()) ? true : false;

        // Destroy current calendar, remove selected date class if it doesn't match
        for (let i = 0; i < date_list.length; i++) {
            date_list[i].innerText = "";
            if (date_list[i].classList.contains("selected-date")) {
                date_list[i].classList.remove("selected-date");
            }
        }
        
        // Construct New Calendar, add selected-date class if we need to.
        let day = 1;
        for (let i = dayOfWeek; i < (dayOfWeek + this.getNumDaysInMonth(month)); i++) {
            date_list[i].innerText = day;
            if (checkForSelectedNode & !init) {
                if (day == this.selected.getDate()) {
                    date_list[i].classList.add("selected-date");
                }
            }
            day++;
        }

        // Set Headers
        this.setCalendarHeader();

        // AJAX to get user deliveries during this month
        getMonthlyDeliveries(this.activeMonth, this.activeYear);
    }

    previousMonth() {
        this.activeMonth = ((this.activeMonth - 1 < 0) ? 11 : this.activeMonth - 1);
        this.activeYear = (this.activeMonth == 11 ? this.activeYear - 1 : this.activeYear);
        this.constructCalendar(this.activeMonth, this.activeYear);
    }

    nextMonth() {
        this.activeMonth = ((this.activeMonth + 1 > 11) ? 0 : this.activeMonth + 1);
        this.activeYear = (this.activeMonth == 0 ? this.activeYear + 1 : this.activeYear);
        this.constructCalendar(this.activeMonth, this.activeYear);
    }

    selectDay(node) {
        // Do not select a day if there is nothing to select.
        if (node.innerText === "") {
            return;
        }

        if (this.selectedNode != null) {
            this.selectedNode.classList.remove("selected-date");
            console.log(this.selectedNode);
        }
        
        node.classList.add("selected-date");
        this.selectedNode = node;
        this.selected = new Date(this.activeYear, this.activeMonth, parseInt(node.innerText));
    }

    setCalendarHeader() {
        this.monthNode.innerText = this.monthNames[this.activeMonth];
        this.yearNode.innerText = this.activeYear;
    }

    getNumDaysInMonth(month) {
        if (month != 1) {
            return this.numDays[this.monthNames[month]];
        }

        // Handle Leap Year (Later tho)
        else {
            return 28;
        }
    }
}

// Performs an AJAX request to get the user deliveries each month. 
function getMonthlyDeliveries(month, year) {
    let monthString = (month + 1 < 10) ? ("0" + (month + 1).toString()) : (month + 1).toString()
    let baseURL = "http://localhost:8000/api/get_monthly_deliveries"
    let requestURL = baseURL + "/" + year.toString() + "/" + monthString;

    $.getJSON(requestURL, function (data) {
        let deliveries = data.deliveries;
        for (let i = 0; i < deliveries.length; i++) {
            console.log(deliveries[i]);
        }
    });
}

var calendar = new JsCalendar();
console.log(calendar.activeMonth);

document.addEventListener("DOMContentLoaded", function(e) {
    document.querySelector('.calendar-previous').addEventListener("click", function() {
        calendar.previousMonth();
    });
    document.querySelector('.calendar-next').addEventListener('click', function() {
        calendar.nextMonth();
    });
    let dateObjects = document.querySelectorAll('.calendar-date');
    for (let i = 0; i < dateObjects.length; i++) {
        dateObjects[i].addEventListener("click", function () {
            calendar.selectDay(dateObjects[i]);
        });
    }
});