import requests

from datetime import datetime

from app.core.modules.hook import Hook
from app.core.modules.quiz_tracker import QuizTracker
from app.core.modules.util import get_answer_status_symbol


def send_post_request(text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://lms.nngasu.ru",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://lms.nngasu.ru/blog/edit.php?action=add",
        "Cookie": "MoodleSession=pr6np242g3fqple3ocnbbm70uv",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "TE": "trailers"
    }

    data = {
        "action": "add",
        "entryid": "",
        "modid": "0",
        "courseid": "0",
        "sesskey": "Fh50hru97B",
        "_qf__blog_edit_form": "1",
        "mform_isexpanded_id_general": "1",
        "mform_isexpanded_id_tagshdr": "1",
        "subject": "Success",
        "summary_editor[text]": f"<p dir=\"ltr\" style=\"text-align: left;\">{text}</p>",
        "summary_editor[format]": "1",
        "summary_editor[itemid]": "228070241",
        "attachment_filemanager": "673895077",
        "publishstate": "site",
        "tags": "_qf__force_multiselect_submission",
        "submitbutton": "Сохранить"
    }

    response = requests.post("https://lms.nngasu.ru/blog/edit.php", headers=headers, data=data)
    return response


def my_lambda_function(quiz_tracker: QuizTracker):
    result = ""
    result += "**********************<br/>"
    result += f"👩🏼‍💻 ID: {quiz_tracker.get_author_id()}<br/><br/>"

    result += f"⌛️ Дата начала: {datetime.fromtimestamp(quiz_tracker.get_start_test())}<br/>"
    result += f"⌛️ Дата окончания: {datetime.fromtimestamp(quiz_tracker.get_end_test())}<br/><br/>"
    result += f"{quiz_tracker.get_gpt_about()}<br/><br/>"

    for question_number, answer in quiz_tracker.get_user_answers().items():
        status = get_answer_status_symbol(answer['success'])
        result += f"💻 {quiz_tracker.get_question_text(question_number)}: "
        result += f"{status} Ответ - {answer['answer']}, "
        result += f"Время - {round(quiz_tracker.get_question_duration(question_number), 2)} сек.<br/><br/>"

    result += f"\n🖥 Score: {quiz_tracker.get_max_score_and_score_player()}\n"
    result += f"🖥 Отзыв GPT: {quiz_tracker.get_gpt_psycho()}<br/>"
    result += "**********************"

    result += f" | score: {quiz_tracker.get_max_score_and_score_player()}"
    send_post_request(result)


Hook.add("test_success", my_lambda_function)
