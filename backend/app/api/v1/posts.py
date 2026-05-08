# schema 검증을 위한 라우터 엔드포인트 구현, FastAPI 서버 생성.
# FastAPI 프레임워크에서 APIRouter, Status 를 불러옴.
# app/schemas/post.py파일에 요청/응답 데이터 규격을 정의한 스키마 불러옴.
# APIRouter를 사용하여 게시판 전용 모듈을 만들거야 주소의 접두사는 /posts를 사용하고 태그는 posts로 표시해
# POST메서드로 posts 라우터 를 생성해 response_model로 PostRead클래스를 사용해, 상태코드는 201을 사용해
# PostCreate (요청) -> PostRead (응답) 구조의 흐름을 설계하는 create_post함수를 만들어줘.
# return PostRead로 응답 결과를 반환해 PostRead 스키마에 객체 id, author_id는 테스트용으로 값 1을 넣어줘.