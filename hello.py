def greet_user():
    name = input("이름을 입력하세요: ").strip()
    if not name:
        name = "Guest"
    print(f"안녕하세요, {name}님!")

def test_greet_user(monkeypatch, capsys):
    # 테스트 1: 이름 입력
    monkeypatch.setattr('builtins.input', lambda _: "Alice")
    greet_user()
    captured = capsys.readouterr()
    assert "안녕하세요, Alice님!" in captured.out

    # 테스트 2: 빈 입력
    monkeypatch.setattr('builtins.input', lambda _: "")
    greet_user()
    captured = capsys.readouterr()
    assert "안녕하세요, Guest님!" in captured.out

if __name__ == "__main__":
    greet_user()
    def test_greet_user():
        pass
     
