import asyncio

destinations = {
    "일본" : 300000,
    "중국" : 500000,
    "베트남" : 400000,
    "미국" : 1800000,
    "스위스" : 1200000
}

seats = [
    {"number": 1, "grade": "이코노미", "extra_price": 0, "reserved": False},
    {"number": 2, "grade": "이코노미", "extra_price": 0, "reserved": True},
    {"number": 3, "grade": "비즈니스", "extra_price": 300000, "reserved": False},
    {"number": 4, "grade": "퍼스트", "extra_price": 700000, "reserved": False}
]

def show_menu():
    print("\n===== 항공권 예약 시스템 =====")
    print("1. 항공권 예약하기")
    print("2. 예약 목록 조회하기")
    print("3. 예약 취소하기")
    print("4. 종료하기")


def select_destination():
    print("\n도착할 국가를 선택해주세요.")
    print("1.일본\n2.중국\n3.베트남\n4.미국\n5.스위스")

    while True:
        destination = input("도착 국가(국가명을 적어주세요): ")

        if destination in destinations:
            return destination, destinations[destination]

        print("잘못된 입력입니다.")


def show_seats():
    print("\n===== 좌석 목록 =====")
    for seat in seats:
        if seat["reserved"] == True:
            status = "이미 예약 되었습니다."
        else :
            status = "예약 가능"

        print(f"{seat["number"]}번 좌석, 등급 : {seat["grade"]}, 추가금 : {seat["extra_price"]}원, {status}")

async def check_seats(seat):
    print("\n좌석 확인 중입니다")
    await asyncio.sleep(1)

    if seat["reserved"] == True:
        return False
    return True


async def select_seat():
    show_seats()

    while True:
        choice = int(input("좌석 번호를 입력하세요. : "))

        for seat in seats:
            if seat["number"] == choice:
                canseat = await check_seats(seat)

                if not canseat:
                    print("이미 예약 되었습니다.")
                    return None

                return seat

        print("존재하지 않는 좌석입니다.")


def select_trip_type():
    while True:
        print("\n여행 유형을 선택하세요")
        print("1. 편도")
        print("2. 왕복")

        choice = int(input("번호 : "))

        if choice == 1:
            return "편도", 1
        elif choice == 2:
            return "왕복", 2
        else:
            print("잘못된 입력입니다.")

def calculate_price(base_price, seat, trip_type_number):
    price = (base_price + seat) * trip_type_number

    return price

reservations = []
reservation_id = 1

async def create_reservation():
    global reservation_id

    print("\n===== 항공권 예약하기 =====")

    name = input("이름을 입력하세요. : ")
    destination, base_price = select_destination()
    seat = await select_seat()
    trip_type, trip_type_number = select_trip_type()
    price = calculate_price(base_price, seat["extra_price"], trip_type_number)


    print("\n===== 예약 확인 =====")
    print(f"이름 : {name}")
    print(f"출발지 : 인천")
    print(f"도착지 : {destination}")
    print(f"좌석 번호 : {seat["number"]}")
    print(f"좌석 등급 : {seat["grade"]}")
    print(f"여행 유형 : {trip_type}")
    print(f"최종 금액 : {price}")

    confirm = input("여행을 확정 하시겠습니까? (y/n) : ")

    if confirm == "y":
        print("예약이 확정 되었습니다")
        seat["reserved"] = True

        reservation = {
            "id" : reservation_id,
            "name": name,
            "departure": "인천",
            "destination": destination,
            "trip_type": trip_type,
            "seat_number": seat["number"],
            "seat_grade": seat["grade"],
            "total_price": price
        }

        reservations.append(reservation)
        reservation_id += 1

    else:
        print("예약이 취소 되셨습니다.")

def show_reservations():
    print("\n===== 예약 목록 =====")

    if len(reservations) == 0:
        print("\n예약 목록이 없습니다.")
        return

    for r in reservations:
        print("\n--------------------")
        print(f'예약 번호 : {r["id"]}')
        print(f'출발지 : {r["departure"]}')
        print(f'도착지 : {r["destination"]}')
        print(f'여행 유형 : {r["trip_type"]}')
        print(f'좌석 번호 : {r["seat_number"]}')
        print(f'좌석 등급 : {r["seat_grade"]}')
        print(f'최종 금액 : {r["total_price"]}원')

def delete_reservation():
    if len(reservations) == 0:
        print("\n취소할 예약이 없습니다.")
        return

    show_reservations()
    del_id = int(input("취소할 예약 번호를 입력하세요. : "))

    for reservation in reservations:
        if reservation["id"] == del_id:
            for seat in seats:
                if seat["number"] == reservation["seat_number"]:
                    seat["reserved"] = False

            reservations.remove(reservation)
            print("예약이 취소되었습니다.")
            return

async def main():
    while True:
        show_menu()
        choice = int(input("메뉴 선택 : "))

        if choice == 1:
            await create_reservation()
        elif choice == 2:
            show_reservations()
        elif choice == 3:
            delete_reservation()
        elif choice == 4:
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

asyncio.run(main())

