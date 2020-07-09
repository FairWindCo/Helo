(function (ELEMENT) {
    ELEMENT.matches = ELEMENT.matches || ELEMENT.mozMatchesSelector || ELEMENT.msMatchesSelector || ELEMENT.oMatchesSelector || ELEMENT.webkitMatchesSelector;
    ELEMENT.closest = ELEMENT.closest || function closest(selector) {
        if (!this) return null;
        if (this.matches(selector)) return this;
        if (!this.parentElement) {
            return null
        } else return this.parentElement.closest(selector)
    };
}(Element.prototype));

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}


function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function click_create_sub_row(event, method = 'POST', modal_target = undefined, modal_target_content = undefined) {
    let [element, show_state] = create_sub_row(event);
    if (event.href) {
        if (show_state) {
            const processor = new AJAXSubFrame(event.href, element, modal_target_content, modal_target, method, false);
            AJAXSubFrame.send_ajax_and_process(event.href, undefined, undefined, undefined, method, function (url, text, ...args) {
                if (element) {
                    element.innerHTML = text;
                    processor.replace_links_to_ajax(element);
                }
            })
        }
        return false;
    } else {
        return element
    }
}

function create_sub_row(currentElement) {
    if (currentElement['sub_element'] !== undefined) {
        let sub_element = currentElement['sub_element'];
        if (sub_element.parentNode.style.display === 'none') {
            sub_element.parentNode.style.display = '';
            return [sub_element, true];
        } else {
            sub_element.parentNode.style.display = 'none';
            return [sub_element, false];
        }
    } else {
        let tr = currentElement.closest('tr');
        if (tr) {
            const id = makeid(10);
            let sub_row = document.createElement('tr');
            let sub_td = document.createElement('td');
            sub_td.colSpan = tr.childElementCount;
            sub_td.id = id;
            sub_row.append(sub_td);
            currentElement['sub_element'] = sub_td;
            currentElement['sub_element_id'] = id;

            insertAfter(tr, sub_row);
            //sub_row.style.display = 'none';
            return [sub_td, true];
        } else {
            return [undefined, false];
        }
    }
}


class AJAXSubFrame {
    constructor(base_url, target, modal_target, modal_dialog, method = 'GET', save_to_history = false) {
        this.base_url = base_url;
        this.modal_target_content = modal_target;
        this.modal_dialog = modal_dialog;
        this.target = target;
        this.method = method;
        this.description = '';
        this.title = '';
        this.save_ajax_to_history = save_to_history
        this.replace_links_to_ajax = this.replace_links_to_ajax.bind(this);
        this.post_processor = this.post_processor.bind(this);
    }

    set_method(method) {
        this.method = method
    }

    set_title(title) {
        this.title = title
    }

    set_description(description) {
        this.description = description
    }

    static add_form_to_request_params(form, searchParams = undefined) {
        if (searchParams === undefined) {
            searchParams = new URL('#').searchParams;
        }
        if (form !== undefined) {
            let formData = new FormData(form);
            formData.set('is_ajax', 'true');
            for (let pair of formData.entries()) {
                searchParams.set(pair[0], pair[1])
            }
        }
        return searchParams;
    }


    static add_string_to_request_params(string_params, searchParams = undefined) {
        if (searchParams === undefined) {
            searchParams = new URL('#').searchParams;
        }
        if (string_params !== undefined) {
            let queryString = new URLSearchParams(string_params);
            for (let pair of queryString.entries()) {
                searchParams.set(pair[0], pair[1])
            }
        }
        return searchParams;
    }

    set_history(url) {
        let query;
        try {
            query = new URL(url);
        } catch (e) {
            query = new URL(self.url);
            AJAXControl.search_to_search_params(query.searchParams, url);
        }
        query.searchParams.delete('is_ajax');
        window.history.pushState(this.description, this.title, query.toString());
    }

    static send_ajax_and_process(url, string_params = undefined, form = undefined, post_data = {}, method = 'POST', post_process = (url, text, ...args) => text, headers = {}, ...args) {
        let [new_url, form_data] = AJAXSubFrame.ajax_url(url, form, string_params, method)
        const csrf = Cookies.get('csrftoken');
        if (csrf) {
            headers['X-CSRFToken'] = csrf;
        }
        let request_params = {
            credentials: 'same-origin',
            method: 'GET',
            headers: headers
        }
        if (method == 'POST') {
            request_params['method'] = 'POST';
            request_params['body'] = Object.assign({}, form_data, post_data);
        }
        fetch(new_url, request_params).then(response => {
            if (response.status === 200) {
                response.text().then(text => {
                    post_process(url, text, ...args);
                });
            }
        });
        return false;
    }

    static send_ajax_request(url, target, post_data = {}, method = 'POST', post_process = (url, text, ...args) => text, headers = {}, ...args) {
        return AJAXSubFrame.send_ajax_and_process(url, undefined, undefined, post_data, method, (u, t, ...a) => {
            let div = target;
            if (target === undefined) {
                div = document.getElementsByTagName('body')
            }
            if (post_process !== undefined) {
                div.innerHTML = post_process(u, t, ...a);
            } else {
                div.innerHTML = text;
            }
        }, headers, ...args);
    }

    do_ajax(url, target, post_data = {}, method = 'POST') {
        return AJAXSubFrame.send_ajax_and_process(url, undefined, undefined, post_data, method, (u, t, ...a) => {
            let div = target;
            if (typeof (target) == 'string') {
                div = document.getElementById(target);
            } else {
                if (target === undefined) {
                    div = document.getElementsByTagName('body')[0];
                }
            }
            div.innerHTML = t;
            if (this.save_ajax_to_history) {
                this.set_history(u);
            }
            this.replace_links_to_ajax(div);
            return div;
        });
    }


    static ajax_url(url, form, string_params, method = 'POST', default_url = '/') {
        let query;
        try {
            query = new URL(url);
        } catch (e) {
            query = new URL(default_url);
            AJAXSubFrame.add_string_to_request_params(url, query.searchParams);
        }
        query.searchParams.set('is_ajax', 'true');
        let post_data = undefined
        if (method === 'POST') {
            if (form !== undefined) {
                let formData = new FormData(form);
                formData.set('is_ajax', 'true');
                const csrf = Cookies.get('csrftoken');
                if (csrf) {
                    formData.set('csrfmiddlewaretoken', csrf);
                }
                post_data = formData;
            }

        } else {
            AJAXSubFrame.add_form_to_request_params(form, query.searchParams);
            post_data = undefined
        }
        AJAXSubFrame.add_string_to_request_params(string_params, query.searchParams);
        return [query, post_data]
    }

    post_processor(url, text, ...args) {
        if (this.save_ajax_to_history) {
            this.set_history(url);
        }
        this.replace_links_to_ajax(text)
        return text;
    }

    replace_links_to_ajax(elements) {
        if (Array.isArray(elements) || ('length' in elements)) {
            for (let x = 0; x < elements.length; x++) {
                const links = elements[x].getElementsByTagName('A');
                this.replace_link_with_ajax(links);
            }
        } else {
            const links = elements.getElementsByTagName('A');
            this.replace_link_with_ajax(links);
        }
    }

    replace_link_with_ajax(elements) {
        for (let x = 0; x < elements.length; x++) {
            const btn = elements[x];
            const self = this;
            const new_querystring = btn.getAttribute('href');
            const open_modal = btn.getAttribute('data-open-modal');
            let target = self.target;
            if (open_modal) {
                btn.setAttribute('data-toggle', 'modal');
                const modal = typeof (self.modal_dialog) == 'string' ? (self.modal_dialog.startsWith('#') ? self.modal_dialog : '#' + self.modal_dialog) : '#' + self.modal_dialog.id
                btn.setAttribute('data-target', modal);
                const modal_content = typeof (self.modal_target_content) == 'string' ? document.getElementById(self.modal_target_content):self.modal_target_content;
                target = modal_content;
            }
            btn.onclick = function (e) {
                e.preventDefault();
                let [url, post_data] = AJAXSubFrame.ajax_url(new_querystring, undefined, undefined, self.method, self.base_url);
                self.do_ajax(url, target, post_data, self.method, self.post_processor);
            }
        }
    }


    static replace_to_ajax(elements, target, open_modal = false, method = 'POST', processor = undefined) {
        for (let x = 0; x < elements.length; x++) {
            const btn = elements[x];
            const self = this;
            let new_querystring = btn.getAttribute('href');
            //let open_modal = btn.getAttribute('open_modal');
            if (open_modal) {
                btn.setAttribute('data-toggle', 'modal');
                btn.setAttribute('data-target', open_modal);
            }

            btn.onclick = function (e) {
                e.preventDefault();
                let [url, post_data] = self.ajax_url(new_querystring, undefined, undefined,);
                AJAXSubFrame.send_ajax_request(url, target, post_data, method, processor);
            };
        }
    }
}