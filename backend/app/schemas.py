from pydantic import BaseModel, Field
class EnrollmentCreate(BaseModel):
    student_id: str = Field(
        min_length=8,
        max_length=8,
        examples=["22000004"],
    )
    class_section_id: str = Field(
        min_length=1,
        max_length=20,
        examples=["WEB-01"],
    )

from typing import Optional, List

# Dành cho Bài 1
class Lecturer(BaseModel):
    id: str
    name: str

# Dành cho Bài 2 (Chi tiết lớp học phần)
class SectionDetail(BaseModel):
    section_id: str
    course_id: str
    course_name: str
    semester_id: str
    lecturer_name: str
    capacity: int
    enrolled: int
    remaining: int

# Dành cho Bài 3 (Cập nhật sức chứa)
class CapacityUpdate(BaseModel):
    capacity: int = Field(gt=0, description="Sức chứa phải là số nguyên lớn hơn 0")