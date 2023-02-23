import enum
import requests


class Token(enum.Enum):
    GUEST = 'guest_token'
    FLOW = 'flow_token'


class Login:
    def __init__(self, username: str, password: str):
        self.session = requests.Session()
        self.session.username = username
        self.session.password = password
        self.session.tokens = {Token.GUEST.value: None, Token.FLOW.value: None}
        self.content = None

    def __get_headers(self) -> dict:
        return {
            "authorization": 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            "content-type": "application/json",
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Vivaldi/4.3',
            "x-guest-token": self.session.tokens[Token.GUEST.value],
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-auth-type": "OAuth2Session" if self.session.cookies.get("auth_token") else '',
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": 'en',
        }

    def __update_token(self, key: str, url: str, payload: dict) -> dict:
        r = self.session.post(url, headers=self.__get_headers(), json=payload).json()
        self.session.tokens[key] = r[key]
        return r

    def init_guest_token(self):
        self.__update_token(Token.GUEST.value, 'https://api.twitter.com/1.1/guest/activate.json', {})

    def flow_start(self):
        self.__update_token(Token.FLOW.value, 'https://api.twitter.com/1.1/onboarding/task.json?flow_name=login', {
            "input_flow_data": {
                "flow_context": {"debug_overrides": {}, "start_location": {"location": "splash_screen"}}
            }, "subtask_versions": {}
        })

    def flow_instrumentation(self):
        self.__update_token(Token.FLOW.value, 'https://api.twitter.com/1.1/onboarding/task.json', {
            "flow_token": self.session.tokens[Token.FLOW.value],
            "subtask_inputs": [{
                "subtask_id": "LoginJsInstrumentationSubtask",
                "js_instrumentation": {"response": "{}", "link": "next_link"}
            }],
        })

    def flow_username(self):
        self.__update_token(Token.FLOW.value, 'https://api.twitter.com/1.1/onboarding/task.json', {
            "flow_token": self.session.tokens[Token.FLOW.value],
            "subtask_inputs": [{
                "subtask_id": "LoginEnterUserIdentifierSSO",
                "settings_list": {
                    "setting_responses": [{
                        "key": "user_identifier",
                        "response_data": {"text_data": {"result": self.session.username}}
                    }], "link": "next_link"}}],
        })

    def flow_password(self):
        self.__update_token(Token.FLOW.value, 'https://api.twitter.com/1.1/onboarding/task.json', {
            "flow_token": self.session.tokens[Token.FLOW.value],
            "subtask_inputs": [{
                "subtask_id": "LoginEnterPassword",
                "enter_password": {"password": self.session.password, "link": "next_link"}}]
        })

    def flow_duplication_check(self):
        r = self.__update_token(Token.FLOW.value, 'https://api.twitter.com/1.1/onboarding/task.json', {
            "flow_token": self.session.tokens[Token.FLOW.value],
            "subtask_inputs": [{
                "subtask_id": "AccountDuplicationCheck",
                "check_logged_in_account": {"link": "AccountDuplicationCheck_false"},
            }],
        })
        self.content = r

    def run(self):
        [fn() for fn in [
            self.init_guest_token,
            self.flow_start,
            self.flow_instrumentation,
            self.flow_username,
            self.flow_password,
            self.flow_duplication_check
        ]]
        return self


def main():
    username = ...
    password = ...

    login = Login(username, password).run()

    print(login.content)
    print(login.session.cookies.get_dict())


if __name__ == '__main__':
    main()
