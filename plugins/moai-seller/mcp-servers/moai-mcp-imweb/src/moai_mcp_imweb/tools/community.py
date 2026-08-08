"""Generated tools — Community (커뮤니티 (폼/Q&A/구매평)). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_all_forms': ('GET', '/community/forms', [], ['page', 'limit', 'unitCode', 'formCreateTimeType', 'formCreateTime', 'formEditTimeType', 'formEditTime'], False),
    'read_one_form': ('GET', '/community/forms/{formNo}', ['formNo'], ['unitCode'], False),
    'read_all_form_submissions': ('GET', '/community/form-submissions', [], ['page', 'limit', 'unitCode', 'formNo', 'formSubmitTimeType', 'formSubmitTime'], False),
    'read_one_form_submission': ('GET', '/community/form-submissions/{submitCode}', ['submitCode'], ['unitCode'], False),
    'read_all_site_qna': ('GET', '/community/qna', [], ['page', 'limit', 'prodCode', 'status', 'qnaCreateTimeType', 'qnaCreateTime'], False),
    'create_site_qna_reply': ('POST', '/community/qna', [], [], True),
    'read_site_qna_answer': ('GET', '/community/qna-answer', [], ['qnaNoList'], False),
    'read_one_site_qna_by_idx': ('GET', '/community/qna/{qnaNo}', ['qnaNo'], [], False),
    'read_all_site_review': ('GET', '/community/review', [], ['page', 'limit', 'prodNo', 'level', 'rating', 'isPhoto', 'reviewCreateTimeType', 'reviewCreateTime'], False),
    'create_site_review': ('POST', '/community/review', [], [], True),
    'read_one_site_review': ('GET', '/community/review/{reviewNo}', ['reviewNo'], [], False),
    'update_site_review_by_review_no': ('PUT', '/community/review/{reviewNo}', ['reviewNo'], [], True),
    'delete_site_review_by_review_no': ('DELETE', '/community/review/{reviewNo}', ['reviewNo'], [], False),
    'read_site_review_answer': ('GET', '/community/review-answer', [], ['reviewNoList'], False),
    'create_site_review_answer': ('POST', '/community/review-answer', [], [], True),
    'delete_site_review_answer_by_review_no': ('DELETE', '/community/review-answer/{reviewAnswerNo}', ['reviewAnswerNo'], [], False),
    'read_all_site_review_by_cursor': ('GET', '/community/review/cursor', [], ['cursor', 'direction', 'limit', 'prodNo', 'level', 'rating', 'isPhoto', 'reviewCreateTimeType', 'reviewCreateTime'], False),
}


class CreateSiteQnaReplyBody(BaseModel):
    """요청 본문 (action='create_site_qna_reply' [POST /community/qna]). 필수 필드: qnaNo, reply, memberUid."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    qnaNo: float = Field(..., description='답변할 Q&A 번호')
    reply: str = Field(..., description='Q&A 답변 내용')
    memberUid: str = Field(..., description='Q&A 답변 작성자 아이디')


class CreateSiteReviewBody(BaseModel):
    """요청 본문 (action='create_site_review' [POST /community/review]). 필수 필드: unitCode, prodNo, body, nick, wtime, rating."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    prodNo: float = Field(..., description='상품번호')
    body: str = Field(..., description='구매평 내용')
    nick: str = Field(..., description='작성자 이름')
    wtime: str = Field(..., description='작성 시각 (ISO 8601 형식). 현재 시각 이후(미래)의 값은 허용되지 않습니다.')
    rating: float = Field(..., description='평점 (1~5점)')
    memberUid: str | None = Field(None, description='회원 ID')
    isHide: str | None = Field(None, description='숨김 여부')
    grade: str | None = Field(None, description='구매평 등급 (1-워스트, 2-일반, 3-베스트)')
    prodOption: str | None = Field(None, description='구매한 상품 옵션 명')
    orderItemCode: str | None = Field(None, description='주문 아이템 코드')
    originReviewId: str | None = Field(None, description='원본 리뷰 ID')
    images: list[str] | None = Field(None, description='리뷰 이미지 파일 (선택, 최대 20개)')


class UpdateSiteReviewByReviewNoBody(BaseModel):
    """요청 본문 (action='update_site_review_by_review_no' [PUT /community/review/{reviewNo}])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    body: str | None = Field(None, description='구매평 내용')
    rating: float | None = Field(None, description='구매평 평점')


class CreateSiteReviewAnswerBody(BaseModel):
    """요청 본문 (action='create_site_review_answer' [POST /community/review-answer]). 필수 필드: reviewNo, unitCode, body, nick, wtime."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    reviewNo: float = Field(..., description='답글을 작성할 구매평 번호')
    unitCode: str = Field(..., description='유닛코드')
    body: str = Field(..., description='구매평 답글 내용')
    nick: str = Field(..., description='작성자 이름')
    wtime: str = Field(..., description='작성 시각 (ISO 8601, UTC). 현재 시각 이후(미래)의 값은 허용되지 않습니다.')
    memberUid: str | None = Field(None, description='회원 ID')
    originReviewId: str | None = Field(None, description='원본 리뷰 ID')

Body = Union[CreateSiteQnaReplyBody, CreateSiteReviewBody, UpdateSiteReviewByReviewNoBody, CreateSiteReviewAnswerBody]

@mcp.tool()
def imweb_community(action: Literal["read_all_forms", "read_one_form", "read_all_form_submissions", "read_one_form_submission", "read_all_site_qna", "create_site_qna_reply", "read_site_qna_answer", "read_one_site_qna_by_idx", "read_all_site_review", "create_site_review", "read_one_site_review", "update_site_review_by_review_no", "delete_site_review_by_review_no", "read_site_review_answer", "create_site_review_answer", "delete_site_review_answer_by_review_no", "read_all_site_review_by_cursor"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""커뮤니티 (폼/Q&A/구매평) 도구 — 17개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 17개 전체 공개).
    params: path + query 파라미터 딕셔너리. 예: {"orderNo": "ORD123", "page": 1}.
    body: POST/PATCH/PUT 본문. action 별 Body 모델(inputSchema anyOf) 중 해당 action 의 필드만 채움 (모델명 = action 의 PascalCase + Body).
    paginate: list 계열 GET 에서 전체 페이지 자동 집계 (기본 False = 단일 페이지).

Returns: API JSON."""
    _method, _path, _pp, _qp, _has_body = _OPS[action]
    _params = params or {}
    _pp_val = {k: _params[k] for k in _pp if k in _params}
    _qp_val = {k: _params[k] for k in _qp if k in _params}
    _client = get_client()
    if paginate and _method == "GET":
        return _client.list_all_pages(_path, params=_qp_val or None)
    _kw = {}
    if _pp_val:
        _kw["path_params"] = _pp_val
    if _qp_val:
        _kw["params"] = _qp_val
    if _has_body:
        _bd = body.model_dump(exclude_none=True, by_alias=True) if body else {}
        _kw["json_body"] = _bd
    return _client.request(_method, _path, **_kw)

