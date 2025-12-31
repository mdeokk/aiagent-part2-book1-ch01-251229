import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 0. 데이터 로드
# -------------------------------
df = pd.read_csv("Incheon_library_202511.csv", encoding="utf-8-sig")

# 컬럼명 확인 (디버깅용)
print("컬럼명:", df.columns.tolist())

# 숫자 변환
df["대출건수"] = pd.to_numeric(df["대출건수"], errors="coerce").fillna(0).astype(int)

# 날짜 변환
df["등록일자"] = pd.to_datetime(df["등록일자"], errors="coerce")

# 분류 컬럼 이름 통일
df = df.rename(columns={"주제분류번호": "category"})


# ==========================================================
# 도전 1. 도서명 기준 대출 건수 Top 10
# ==========================================================
top10_books = (
    df["도서명"]
    .value_counts()
    .head(10)
    .reset_index()
)
top10_books.columns = ["도서명", "대출건수"]

top10_books.to_csv("top10_books_by_loan.csv", index=False, encoding="utf-8-sig")

print("\n[도전1] 도서명 기준 대출 TOP 10")
print(top10_books)



# ==========================================================
# 도전 2. 분류 기준 대출 현황 집계
# ==========================================================
loan_by_category = (
    df.groupby("category", as_index=False)
      .agg(
          대출건수합계=("대출건수", "sum"),
          평균대출건수=("대출건수", "mean")
      )
      .sort_values("대출건수합계", ascending=False)
)

loan_by_category.to_csv("loan_by_category.csv", index=False, encoding="utf-8-sig")

print("\n[도전2] 분류 기준 대출 현황")
print(loan_by_category.head(10))



# ==========================================================
# 도전 3. 월별 대출 추이 그래프 생성
# ==========================================================
df["월"] = df["등록일자"].dt.to_period("M").astype(str)
monthly = df.groupby("월").size().reset_index(name="대출건수")

# 그래프 출력
plt.figure(figsize=(12,5))
plt.plot(monthly["월"], monthly["대출건수"], marker="o")
plt.xticks(rotation=45)
plt.title("월별 대출 건수 추이")
plt.xlabel("월")
plt.ylabel("대출건수")
plt.grid(True)
plt.tight_layout()
plt.savefig("loan_monthly_trend.png")  # 그래프 저장
plt.close()

print("\n[도전3] 월별 대출 추이 그래프 생성 완료 (loan_monthly_trend.png 저장 완료)")



# ==========================================================
# 도전 4. AI Agent 입력용 요약 데이터 생성
# ==========================================================
total_loans = len(df)

top_book = df["도서명"].value_counts().idxmax()

top_category = df.groupby("category")["대출건수"].sum().idxmax()

top_month = df["월"].value_counts().idxmax()

summary = pd.DataFrame([{
    "전체대출건수": total_loans,
    "최다대출도서": top_book,
    "최다대출분류": top_category,
    "대출최다월": top_month
}])

summary.to_csv("loan_summary_for_llm.csv", index=False, encoding="utf-8-sig")

print("\n[도전4] AI Agent 입력용 요약 데이터 생성 완료")
print(summary)

print("\n=== 전체 작업 완료! ===")
