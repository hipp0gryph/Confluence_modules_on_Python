from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# use for html watch and fastapi jinja templates work
import jinja2

from cruds.crud_group import read_all_groups
from cruds.crud_marks import read_marks_with_student_name
from cruds.crud_achievements import read_achievements_with_names

print(jinja2.__version__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(path="/marks_html", response_class=HTMLResponse, tags=['html'])
async def marks_html(request: Request):
    groups = read_all_groups()
    marks = read_marks_with_student_name()
    return templates.TemplateResponse("marks.html", {"request": request, "groups": groups, "marks": marks})


@router.get(path="/achievement_html", response_class=HTMLResponse, tags=['html'])
async def achievement_html(request: Request):
    achievements = read_achievements_with_names()
    return templates.TemplateResponse("achievement.html", {"request": request, "achievements": achievements, "zip": zip})
