"""Cafe24 Admin API — Community domain (게시판).

게시판(boards) + 게시물(articles) + 댓글(comments) + SEO + 자주쓰는답변(commenttemplates)
+ 월별 리뷰 통계(monthlyreviews) + 긴급문의(urgentinquiry).

Scopes: ``mall.read_community`` / ``mall.write_community``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "community"
_R = "mall.read_community"
_W = "mall.write_community"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int", description="최대건수 (최대 100)"), Param("offset", type="int"))

register(
    # === Boards ===
    Endpoint(name="cafe24_board_list", category=_C, method="GET", path=f"{_A}/boards", scope=_R,
             summary="게시판 목록", resource_key="board", list_endpoint=True),
    Endpoint(name="cafe24_board_get", category=_C, method="GET", path=f"{_A}/boards/{{board_no}}", scope=_R,
             summary="게시판 설정 조회", resource_key="board"),
    Endpoint(name="cafe24_board_update", category=_C, method="PUT", path=f"{_A}/boards/{{board_no}}", scope=_W,
             summary="게시판 설정 수정", resource_key="board", takes_body=True),
    Endpoint(name="cafe24_board_seo_get", category=_C, method="GET", path=f"{_A}/boards/{{board_no}}/seo", scope=_R,
             summary="게시판 SEO 조회", resource_key="board_seo"),
    Endpoint(name="cafe24_board_seo_update", category=_C, method="PUT", path=f"{_A}/boards/{{board_no}}/seo", scope=_W,
             summary="게시판 SEO 수정", resource_key="board_seo", takes_body=True),

    # === Articles (게시물) ===
    Endpoint(name="cafe24_article_list", category=_C, method="GET", path=f"{_A}/boards/{{board_no}}/articles", scope=_R,
             summary="게시물 목록", resource_key="article", list_endpoint=True,
             query_params=_LIST + (Param("start_date"), Param("end_date"), Param("search", description="subject/content/writer_name/product/member_id"),
                                   Param("keyword"), Param("reply_status", description="N/P/C"), Param("product_no"))),
    Endpoint(name="cafe24_article_create", category=_C, method="POST", path=f"{_A}/boards/{{board_no}}/articles", scope=_W,
             summary="게시물 등록 (필수: writer/title/content/client_ip)", resource_key="article", takes_body=True, body_key="articles"),
    Endpoint(name="cafe24_article_update", category=_C, method="PUT", path=f"{_A}/boards/{{board_no}}/articles/{{article_no}}", scope=_W,
             summary="게시물 수정", resource_key="article", takes_body=True),
    Endpoint(name="cafe24_article_delete", category=_C, method="DELETE", path=f"{_A}/boards/{{board_no}}/articles/{{article_no}}", scope=_W,
             summary="게시물 삭제", resource_key="article"),

    # === Comments ===
    Endpoint(name="cafe24_article_comment_list", category=_C, method="GET", path=f"{_A}/boards/{{board_no}}/articles/{{article_no}}/comments", scope=_R,
             summary="게시물 댓글 목록", resource_key="comment", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_article_comment_create", category=_C, method="POST", path=f"{_A}/boards/{{board_no}}/articles/{{article_no}}/comments", scope=_W,
             summary="댓글 등록 (필수: content/writer/password)", resource_key="comment", takes_body=True),
    Endpoint(name="cafe24_article_comment_delete", category=_C, method="DELETE", path=f"{_A}/boards/{{board_no}}/articles/{{article_no}}/comments/{{comment_no}}", scope=_W,
             summary="댓글 삭제", resource_key="comment"),
    Endpoint(name="cafe24_board_comment_list", category=_C, method="GET", path=f"{_A}/boards/{{board_no}}/comments", scope=_R,
             summary="게시판 댓글 일괄 조회 (since_comment_no 기반)", resource_key="comment", list_endpoint=True,
             query_params=(Param("since_comment_no", type="int"), Param("limit", type="int"))),

    # === Comment templates (자주쓰는답변) ===
    Endpoint(name="cafe24_commenttemplate_list", category=_C, method="GET", path=f"{_A}/commenttemplates", scope=_R,
             summary="자주쓰는 답변 목록", resource_key="commenttemplate", list_endpoint=True,
             query_params=(Param("board_type", type="int"), Param("title"))),
    Endpoint(name="cafe24_commenttemplate_get", category=_C, method="GET", path=f"{_A}/commenttemplates/{{comment_no}}", scope=_R,
             summary="자주쓰는 답변 상세", resource_key="commenttemplate"),
    Endpoint(name="cafe24_commenttemplate_create", category=_C, method="POST", path=f"{_A}/commenttemplates", scope=_W,
             summary="자주쓰는 답변 생성 (필수: title/content/board_type)", resource_key="commenttemplate", takes_body=True),
    Endpoint(name="cafe24_commenttemplate_update", category=_C, method="PUT", path=f"{_A}/commenttemplates/{{comment_no}}", scope=_W,
             summary="자주쓰는 답변 수정", resource_key="commenttemplate", takes_body=True),
    Endpoint(name="cafe24_commenttemplate_delete", category=_C, method="DELETE", path=f"{_A}/commenttemplates/{{comment_no}}", scope=_W,
             summary="자주쓰는 답변 삭제", resource_key="commenttemplate"),

    # === Monthly reviews ===
    Endpoint(name="cafe24_monthlyreview_list", category=_C, method="GET", path=f"{_A}/financials/monthlyreviews", scope=_R,
             summary="월별 리뷰 통계 (특정클라이언트)", resource_key="financial_monthlyreview", list_endpoint=True,
             query_params=(Param("start_month", required=True), Param("end_month", required=True))),

    # === Urgent inquiry (긴급문의) ===
    Endpoint(name="cafe24_urgentinquiry_list", category=_C, method="GET", path=f"{_A}/urgentinquiry", scope=_R,
             summary="긴급문의 게시물 목록", resource_key="urgentinquiry", list_endpoint=True,
             query_params=_LIST + (Param("start_date"), Param("end_date"))),
    Endpoint(name="cafe24_urgentinquiry_reply_get", category=_C, method="GET", path=f"{_A}/urgentinquiry/{{article_no}}/reply", scope=_R,
             summary="긴급문의 답변 조회", resource_key="urgentinquiry_reply", list_endpoint=True),
    Endpoint(name="cafe24_urgentinquiry_reply_create", category=_C, method="POST", path=f"{_A}/urgentinquiry/{{article_no}}/reply", scope=_W,
             summary="긴급문의 답변 등록", resource_key="urgentinquiry_reply", takes_body=True),
    Endpoint(name="cafe24_urgentinquiry_reply_update", category=_C, method="PUT", path=f"{_A}/urgentinquiry/{{article_no}}/reply", scope=_W,
             summary="긴급문의 답변 수정", resource_key="urgentinquiry_reply", takes_body=True),
)
