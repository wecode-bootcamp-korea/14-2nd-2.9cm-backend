# 14-2nd-2.9cm-backend
# Introduction
사진추가 예정
> 진행기간: 2020.11.30 ~ 2020.12.12 (13일)
- __팀명__ : 2.9cm
- __목적__ : 의류를 기반으로 한 온라인 종합쇼핑몰 [29CM](https://www.29cm.co.kr/home/)를 클론하면서 개발과 협업의 역량을 향상시킨다.
- __29cm 사이트 특징__ : 의류를 기반으로 한 온라인 종합쇼핑몰 입니다. 하지만, 옷만 판매하는 일반 쇼핑몰과는 달리 사용자의 라이프스타일과 취향을 분석하고 셀렉팅하여 차별성을 두었습니다. 일상과 설렘의 간격을 표현한 브랜드 네임처럼 여행, 문화, 쇼핑 등 다양한 테마를 중심으로 이용자와 소통을 시도하며, 우리나라 대표적인 미디어 커머스 입니다. SNS 느낌의 29TV나 블로그 형식의 Welove라는 자체 콘텐츠들도 발행하고 있어 매거진 기능도 겸하고 있습니다, 디자인도 직관적이고 깔끔하며 사용자 편의에 맞춘 UI가 인상적입니다.
- __Scrum 방식으로 진행__ : 일주일 단위로 Sprint를 나누고, 주간 미팅과 데일리 스탠딩 미팅을 통해 각 팀원의 진행사항 및 계획에 대해 공유하며 진행하였습니다.
## Team Members
🐶 __Front-end__ ([github repo](https://github.com/wecode-bootcamp-korea/14-2nd-2.9cm-frontend))
- 김태현 - [github](https://github.com/pepekim)
- 박현재 - [github](https://github.com/J-Bback)

🐼 __Back-end__ ([github repo](https://github.com/wecode-bootcamp-korea/14-2nd-2.9cm-backend))
- 김영주(PM) - [github](https://github.com/097kim)
- 강두연 - [github](https://github.com/dooyeonk)
- 김영환 - [github](https://github.com/ohwani)

# 적용 기술
- Front-end
  - React.js(Hooks)
  - Styled Component
  - React-router
  - React-slick
- Back-end
  - Python
  - Django
  - MySQL
  - JWT, Bcrypt
  - Django Test, Mock
  - Git & GitHub (Rebase 활용)
  - AWS EC2, AWS RDS
  - Docker

# 브랜치 관리 전략
__Git Flow__ 사용하여 브랜치를 관리합니다.<br>
![](https://www.campingcoder.com/post/20180412-git-flow.png)
진행 기간동안 모든 브랜치는 Pull Request에 리뷰를 진행한 후 merge를 진행합니다.

Master : 배포시 사용합니다. <br>
Develop : 완전히 개발이 끝난 부분에 대해서만 Merge를 진행합니다. <br>
Feature/feacture1 : 기능 개발을 진행할 때 사용합니다.

# Modelling
![](https://images.velog.io/images/dooyeonk/post/4079151c-db69-4154-84f1-401c95f9fb6d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202020-12-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.28.51.png)

# What We Did
- 모델링 \[Aquery Tool]
- 회원가입 \[bcrypt (DB에 암호화된 비밀번호 저장)]
- 로그인 \[bcrpyt (비밀번호 대조), JWT(토큰 생성)]
- 소셜로그인 \[NAVER, KAKAO, GOOGLE Open API]
- 로그인 확인 데코레이터 [JWT (토큰 복호화)]
- 상품 리스트 엔드포인트 구현 (필터링 포함)
- 핸드폰 문자인증 기능 추가 [NAVER CLOUD PLATFORM API]
- 장바구니
- 상품 리스트 검색, 페이지네이션
- 상품 상세페이지
- 상품 리뷰
- Unit Test 작성 및 테스트 완료
- AWS RDS 구축 및 EC2 & Docker 사용하여 배포

# API
[구글 docs API Documentation](https://docs.google.com/document/d/1bpR_FZsrh9u4kUOok08F3VmEyIqqtRsoZpprnRQi9BU/edit?usp=sharing)
- 김영주 (PM)
  - 작성하세요
  
- 강두연
  - \[일반 회원가입] POST /user/signup
  - \[일반 로그인] POST /user/login
  - \[네이버]소셜 로그인 POST /user/login/naver
  - \[카카오]소셜 로그인 POST /user/login/kakao
  - \[구글]소셜 로그인 POST /user/login/google
  - \[핸드폰 문자 인증 (문자 보내기)] POST /user/sms
  - \[문자 인증 확인 및 유저 상세정보 저장] POST /user/details

- 김영환
  - 장성하세요

## 레퍼런스
- 이 프로젝트는 [29CM](https://www.29cm.co.kr/home/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.



