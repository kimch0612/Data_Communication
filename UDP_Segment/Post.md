# UDP 세그먼트 실습

## INDEX
1. [이 실습을 진행하는 목적](#1-이-실습을-진행하는-목적)
2. [실습 전 준비사항](#2-실습-전-준비사항)
3. [Gateway로 파일을 보낸 경우](#3-gateway로-파일을-보낸-경우)
4. [HeX값 수정해보기](#4-hex값-수정해보기)
5. [마무리](#5-마무리)
---
### 1. 이 실습을 진행하는 목적
- 패킷은 한 번에 보낼 수 있는 사이즈가 정해져있는데, 그보다 큰 파일을 전송할 시에 운영체제가 패킷을 어떻게 핸들링 하는지, 그리고 제가 배우고 기억한 내용이 맞는지에 대해서 확인하고자 합니다.
- 실습에 들어가기 앞서, 지난 시간에 배운 내용을 바탕으로 이론을 정리해보자면 다음과 같습니다.
  - 위에서 언급했듯이 패킷은 한번에 보낼 수 있는 최대의 사이즈가 1460Bytes로 정해져있습니다. 이것을 Maximum Segment Size (a.k.a. MSS)라고 합니다.
  - MSS보다 큰 사이즈를 사용자가 수/송신하고자 한다면 OSI 4계층에 의해 패킷이 Slice되게 되는데, 이러한 이유로 4계층을 Segment라고 부릅니다.
  - Slice된 패킷에는 앞쪽에 Header가 추가로 붙게 되는데, UDP가 TCP보다 Header의 크기가 상대적으로 작으므로 (TCP의 경우에는 20Bytes+@이지만 UDP는 8Bytes) UDP가 TCP에 비해 비교적 더 빠르고 원할한 통신을 할 수 있습니다.
  - Slice된 패킷의 Header를 살펴보면 맨 마지막 패킷을 제외한 그 외의 패킷들에겐 자신이 어떤 프로토콜로 통신중인지 명시돼있지 않으며, 맨 마지막 패킷에 프로토콜이 명시돼있습니다.
  - 맨 마지막 패킷에는 프로토콜뿐 아니라 Slice된 Data의 사이즈와 패킷을 재조합했을 때의 사이즈도 명시돼있습니다.
---
### 2. 실습 전 준비사항
- 패킷을 보내는 프로그램으로는 [Packet Sender](https://packetsender.com/)를 이용할 것이며, 전송할 파일은 [대학의 공식 로고 이미지](https://nsu.ac.kr/res/service/img/common/btn_logo_header.png)를 이용할 것입니다.
- 패킷을 보낼 서버는 다음과 같습니다.

| Server | Adress | Port |
|:---|:---|:---|
| L3 Gateway | 172.30.1.254 | 6000 |
---
### 3. Gateway로 파일을 보낸 경우
- Packet Sender를 다음과 같이 설정했습니다.

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/563385cd-6db4-401b-adf6-70c08abaf4c3)
- Wireshark에서 아래의 필터 옵션을 넣은 상태로 Packet Sender에서 Send를 눌렀을때의 결과창입니다.
```
ip.addr==172.30.1.254 && ip.proto==UDP && !ssdp

#ip.addr==172.30.1.254: 172.30.1.254와 통신한 패킷만 출력합니다.
#ip.proto==UDP: 통신할 때 사용된 프로토콜이 UDP인 패킷만 출력합니다.
                교수님께서 제공해주신 자료에는 udp라고 작성돼있는데,
                소문자로 작성하니 오류가 나는 관계로 대문자로 작성했습니다.
#!ssdp: 프로토콜이 ssdp인 패킷은 출력되지 않게 막습니다.

#리눅스/유닉스 또는 프로그래밍 언어에서 자주 사용했던 Pipeline과 Not 연산자를 이곳에서도 사용할 수 있다는 것을 처음으로 알았습니다.
``` 

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/029e86ef-cccd-4cc2-a0ce-6070914208dd)
- 패킷을 자세히 보면 "Fragmented"라고 표시돼있는 것을 확인할 수 있는데, 제가 배웠던 이론대로 조각난(Fragmented)것을 알 수 있었습니다.

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/9d679e9b-32bf-40a3-96ea-f9d8d2e66c86)
- 이번에는 Protocol을 확인해보니 제가 기억하고 있는 대로 맨 마지막 패킷을 제외하고는 전부 IPv4로 기재돼있는 것을 확인할 수 있었습니다.
- Length의 경우에는 각각의 패킷의 사이즈는 1514Bytes, 전송된 데이터의 사이즈는 1480Bytes로 나왔습니다.
- 다만 제가 생각한 대로라면 패킷의 총 사이즈가 1460Bytes를 넘으면 안 될 것 같은데, 이 패킷들은 그 사이즈를 넘긴게 이상해서 MSS 관련 Reference를 찾아보았더니 이건 TCP에서만 사용하는 매커니즘이라는 것을 알게되었습니다.
  - TCP는 연결 지향성과 신뢰성이라는 특성을 제공하기 위해 세부적인 설정과 관리가 필요하며, 그렇기 때문에 MSS와 같은 매커니즘이 사용된다고 합니다.
  - UDP의 경우에는 별도로 MSS를 정의하지 않았기 때문에 원래는 패킷이 Slice되지 않는게 맞는데, 네트워크 / 운영체제 시스템의 MTU값에 따라 패킷을 Slice하기 때문에 결국에는 Fragmented 되는 것이라고 합니다.
  - [참고문헌 1](https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-mss/) / [참고문헌 2](https://ejjoo.github.io/network/2020/01/09/tcp-mss-udp.html)

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/e2ac5ee9-9dc4-4f16-b70f-886ed8b1dcfe)
- 위에서 확인한 내용을 검증해보기 위해 이번에는 MTU의 값을 변경해서 패킷을 전송해보았습니다. MTU의 값을 1000으로 변경해보았더니 패킷의 사이즈들이 정말로 감소한 것을 확인할 수 있었습니다.

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/f2b9da9c-950e-469c-91fe-18b20ee54a7f)
- 이번에는 맨 처음 패킷과 맨 마지막 패킷을 분석해보았습니다.
- 맨 처음 패킷은 제가 기억하고 있는 대로 Protocol에 대한 내용이 기재되어있지 않았으며, Slice된 Data에 대해서도 기재되어 있었습니다.
- 맨 마지막 패킷에는 UDP에 대한 내용이 기재되어 있었으며, 총 Data와 패킷의 사이즈 또한 기재되어 있었습니다.
  - 총 Data의 사이즈는 10922Bytes이고, 패킷은 10930Bytes이므로 UDP의 Header가 8Bytes라고 배운 것도 확인할 수 있었습니다.

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/fa295add-c7b2-45a0-bc92-9d7bcf28df58)
![image](https://github.com/kimch0612/Data_Communication/assets/10193967/66c40976-0118-49a1-9094-5fe3772085b5)
- 마지막으로 패킷을 받은 서버가 보낸 응답 패킷을 확인해보았습니다.
- 패킷을 보낸 목적지는 존재하나, 6000번 포트는 열려있지 않으므로 (서비스하고 있지 않으므로) Port unreachable 응답을 받은걸 확인할 수 있었습니다. 

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/005df1f2-8735-4b37-b31d-300eee78ea50)
- 마지막으로, 전송이 불가능한 경우의 패킷이 아니라 실제로 전송에 성공한 패킷을 보고 싶어서 간단하게 파이썬으로 UDP 소켓 프로그램을 작성해서 테스트해 보았습니다.
- 위와 다르게 까만색 ICMP 메시지가 안 뜨고 MTU값(1500)에 따라 잘 전송된 것을 확인할 수 있었습니다.

![image](https://github.com/kimch0612/Data_Communication/assets/10193967/275858de-5f02-426e-b76c-6be8bfcf8f0a)
---
### 4. HeX값 수정해보기
---
### 5. 마무리
---