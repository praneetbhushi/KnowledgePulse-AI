from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.search_query import SearchQuery
from datetime import datetime, timedelta
from sqlalchemy import func, case

router = APIRouter()

@router.get("/trends")
def get_analytics_trends(
    db: Session = Depends(get_db),
):
    today = datetime.utcnow().date()
    seven_days_ago = today - timedelta(days=6)

    results = (
        db.query(
            func.date(SearchQuery.searched_at).label("date"),

            func.count(SearchQuery.id).label("searches"),

            func.sum(
                case(
                    (SearchQuery.was_answered.is_(True), 1),
                    else_=0,
                )
            ).label("answered"),

            func.sum(
                case(
                    (SearchQuery.was_answered.is_(False), 1),
                    else_=0,
                )
            ).label("unanswered"),

            func.avg(SearchQuery.search_time).label(
                "average_search_time"
            ),

            func.avg(SearchQuery.llm_time).label(
                "average_llm_time"
            ),

            func.avg(SearchQuery.total_rag_time).label(
                "average_rag_time"
            ),
        )
        .filter(
            SearchQuery.searched_at >= seven_days_ago
        )
        .group_by(
            func.date(SearchQuery.searched_at)
        )
        .order_by(
            func.date(SearchQuery.searched_at)
        )
        .all()
    )

    result_map = {
        str(row.date): {
            "date": str(row.date),
            "searches": int(row.searches or 0),
            "answered": int(row.answered or 0),
            "unanswered": int(row.unanswered or 0),
            "average_search_time": round(
                float(row.average_search_time or 0), 2
            ),
            "average_llm_time": round(
                float(row.average_llm_time or 0), 2
            ),
            "average_rag_time": round(
                float(row.average_rag_time or 0), 2
            ),
        }
        for row in results
    }

    trends = []

    for i in range(7):
        current_date = seven_days_ago + timedelta(days=i)
        date_string = str(current_date)

        if date_string in result_map:
            trends.append(result_map[date_string])
        else:
            trends.append({
                "date": date_string,
                "searches": 0,
                "answered": 0,
                "unanswered": 0,
                "average_search_time": 0,
                "average_llm_time": 0,
                "average_rag_time": 0,
            })

    return trends

# ============================================================
# Analytics Dashboard
# ============================================================

@router.get("/dashboard")
def get_analytics_dashboard(
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Total searches
    # --------------------------------------------------------

    total_searches = (
        db.query(func.count(SearchQuery.id))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Answered searches
    # was_answered = True
    # --------------------------------------------------------

    answered_searches = (
        db.query(func.count(SearchQuery.id))
        .filter(SearchQuery.was_answered.is_(True))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Unanswered searches
    # was_answered = False
    # --------------------------------------------------------

    unanswered_searches = (
        db.query(func.count(SearchQuery.id))
        .filter(SearchQuery.was_answered.is_(False))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Answer rate
    # --------------------------------------------------------

    answer_rate = (
        (answered_searches / total_searches) * 100
        if total_searches > 0
        else 0
    )

    # --------------------------------------------------------
    # Average search time
    # --------------------------------------------------------

    avg_search_time = (
        db.query(func.avg(SearchQuery.search_time))
        .filter(SearchQuery.search_time.isnot(None))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Average LLM generation time
    # --------------------------------------------------------

    avg_llm_time = (
        db.query(func.avg(SearchQuery.llm_time))
        .filter(SearchQuery.llm_time.isnot(None))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Average RAG execution time
    # --------------------------------------------------------

    avg_rag_time = (
        db.query(func.avg(SearchQuery.total_rag_time))
        .filter(SearchQuery.total_rag_time.isnot(None))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Average semantic distance
    # --------------------------------------------------------

    avg_distance = (
        db.query(func.avg(SearchQuery.best_distance))
        .filter(SearchQuery.best_distance.isnot(None))
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "total_searches": int(total_searches),
        "answered_searches": int(answered_searches),
        "unanswered_searches": int(unanswered_searches),
        "answer_rate": round(float(answer_rate), 2),

        "average_search_time": round(
            float(avg_search_time),
            2,
        ),

        "average_llm_time": round(
            float(avg_llm_time),
            2,
        ),

        "average_rag_time": round(
            float(avg_rag_time),
            2,
        ),

        "average_distance": round(
            float(avg_distance),
            3,
        ),
    }

# ============================================================
# Recent Searches
# ============================================================

@router.get("/recent-searches")
def get_recent_searches(
    db: Session = Depends(get_db),
):
    searches = (
        db.query(SearchQuery)
        .order_by(SearchQuery.searched_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": search.id,
            "query": search.query,

            "was_answered": search.was_answered,

            "result_count": search.result_count,
            "best_distance": search.best_distance,

            "search_time": search.search_time,
            "llm_time": search.llm_time,
            "total_rag_time": search.total_rag_time,

            # Frontend expects this exact field name
            "searched_at": search.searched_at,
        }
        for search in searches
    ]