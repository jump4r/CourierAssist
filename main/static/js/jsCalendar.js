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

        // Displayed in a monthly format, so we need a current month/year var
        this.activeMonth = this.selected.getMonth();
        this.activeYear = this.selected.getFullYear();

        this.constructCalendar(this.activeMonth, this.activeYear);
    }

    constructCalendar(month, year) {
        let first = new Date(year, month, 1);
        let dayOfWeek = first.getDay();

        let date_list = document.querySelectorAll(".calendar-date");

        // Destroy Calendar
        for (let i = 0; i < date_list.length; i++) {
            date_list[i].innerText = "";
        }
        
        // Construct New Calendar
        let day = 1;
        for (let i = dayOfWeek; i < (dayOfWeek + this.getNumDaysInMonth(month)); i++) {
            date_list[i].innerText = day;
            day++;
        }
    }

    previousMonth() {
        this.activeMonth = ((this.activeMonth - 1 < 0) ? 11 : this.activeMonth - 1);
        this.activeYear = (this.activeMonth == 11 ? this.activeYear - 1 : this.activeYear);

        console.log(this.activeMonth + ", " + this.activeYear);
        this.constructCalendar(this.activeMonth, this.activeYear);
    }

    nextMonth() {
        this.activeMonth = ((this.activeMonth + 1 > 11) ? 0 : this.activeMonth + 1);
        this.activeYear = (this.activeMonth == 0 ? this.activeYear + 1 : this.activeYear);

        console.log(this.activeMonth + ", " + this.activeYear);
        this.constructCalendar(this.activeMonth, this.activeYear);
    }

    selectDay(node) {
        // Do not select a day if there is nothing to select.
        console.log(node);
        
        if (node.innerText === "") {
            return;
        }
        if (this.selectedNode != null) {
            this.selectedNode.classList.remove("selected-date");
        }
        
        node.classList.add("selected-date");
        this.selectedNode = node;
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