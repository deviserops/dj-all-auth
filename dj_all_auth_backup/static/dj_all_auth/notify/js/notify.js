class Notify {
    constructor(conf = null) {
        if (typeof window !== 'undefined') {
            // Running in a browser environment
            window._notify = this;
        } else if (typeof global !== 'undefined') {
            // Running in a Node.js environment
            global._notify = this;
        }


        let custom_html = conf && conf.html ? conf.html : null
        let position = conf && conf.position ? conf.position : null
        this.config = {
            title: !(conf && conf.title === false),
            icon: !(conf && conf.icon === false),
            html: _notify.html_layout(custom_html),
            timeout: conf && conf.timeout ? conf.timeout : 4000, // auto remove timeout (in ms),
            position: _notify.positions(position)
        }
    }

    registerRemoveEvents() {
        let _notify_area = document.getElementsByClassName("notify__area")
        for (const [key, element] of Object.entries(_notify_area)) {
            element.addEventListener('click', function () {
                _notify.removeAnimate(element, 0)
            })
        }
    }

    positions(position) {
        let positions = ['top-left', 'top-right', 'top-center', 'bottom-left', 'bottom-center', 'bottom-right', 'left-middle', 'right-middle', 'center-middle']
        return positions.includes(position) ? position : 'top-right'
    }

    types() {
        return {
            'danger': ['danger', 'error'],
            'info': ['information', 'info', 'message'],
            'success': ['success'],
            'warning': ['warning'],
            'notice': ['notice']
        }
    }

    show(type = 'info', message = null, title = null) {
        let type_list = _notify.types()
        let type_to_use = 'info'
        for (let list in type_list) {
            type_to_use = type_list[list].includes(type) ? list : type_to_use
        }

        //html
        _notify.append_html()   // add notify defailt and hide it
        _notify.append_notify_type(type_to_use, type) // append appropriate class according to notification to apply css
        _notify.append_notify_message(message)
        _notify.display_notify()
        //display noty
        _notify.registerRemoveEvents()
    }

    append_html() {
        let default_html = _notify.config.html
        let container = document.getElementsByClassName('notify__container')[0]
        if (container) {
            container.insertAdjacentHTML('beforeend', default_html)
        } else {
            let container = document.createElement('div')
            container.className = 'notify__container ' + _notify.config.position
            container.innerHTML = default_html
            let html_body = document.getElementsByTagName('body')[0]
            html_body.append(container)
        }
        /**
         * Hide default last element that is added so we can add css, class and message to notify
         *
         * Once all added we will display this
         */
        container = document.getElementsByClassName('notify__container')[0]
        container.lastElementChild.style.display = 'none'
    }

    append_notify_type(type_to_use, type) {
        let container = document.getElementsByClassName('notify__container')[0]
        container.lastElementChild.className += ' notify__' + type_to_use

        /**
         * set icon and title if config
         * @type {string}
         */
        if (!_notify.config.icon) {
            container.lastElementChild.getElementsByClassName('notify__icon')[0].style.display = 'none'
        }
        if (!_notify.config.title) {
            container.lastElementChild.getElementsByClassName('notify__title')[0].style.display = 'none'
        } else {
            container.lastElementChild.getElementsByClassName('notify__title')[0].textContent = type
        }
    }

    append_notify_message(message) {
        let container = document.getElementsByClassName('notify__container')[0]
        container.lastElementChild.getElementsByClassName('notify__message')[0].innerHTML = message
    }

    display_notify() {
        let container = document.getElementsByClassName('notify__container')[0]
        container.lastElementChild.style.display = 'block'
        _notify.applyAnimate(container.lastElementChild)

    }

    applyAnimate(element) {
        // psudo element (::after) for progress bar
        let progressBarTimeout = _notify.config.timeout

        /**
         * Because css take time on browser so apply little timeout for animation
         */
        setTimeout(function () {
            // Animation effect slide from top
            element.style.setProperty('--notifyAreaHeight', 'auto')
            element.style.setProperty('--notifyAreaPadding', '10px 10px')

            // bar animation
            element.style.setProperty('--jsProgressBarWidth', '0')
            element.style.setProperty('--jsProgressBarTimeout', 'all ' + progressBarTimeout + 'ms linear 0s')

            _notify.removeAnimate(element)
        }, 100)
    }

    removeAnimate(element, time = null) {
        /**
         * Remove First Element after timeout is completed
         * Also Apply animation before removing element
         */
        let timeout = time != null ? time : _notify.config.timeout
        setTimeout(function () {
            element.style.setProperty('--notifyAreaHeight', '0')
            element.style.setProperty('--notifyAreaPadding', '0 10px')
            setTimeout(function () {
                element.remove()
            }, 500)
        }, timeout)
    }

    html_layout(html = null) {
        if (html) {
            return html
        }
        return '<div class="notify__area"><div class="notify__icon"></div><div class="notify__content">' +
            '<div class="notify__title"></div><div class="notify__message"></div></div></div>'
    }
}