from rest_framework import serializers
from  .models import Resume,Skill
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields=[
            "id",
            "user",
            "file",
            "original_filename",
            "extracted_text",
            "skills",
            "uploaded_at",
            "updated_at"
        ]
        read_only_fields=[
            "id",
            "user",
            "original_filename",
            "extracted_text",
            "skills",
            "uploaded_at",
            "updated_at"
        ]
    def validate_file(self,value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.validationError("only pdf allowed")
        max_size=5*1024*1024
        if value.size>max_size:
            raise serializers.validationError("Resume must be 5mb or less")
        try:
            import fitz
            value.seek(0)
            pdf=fitz.open(stream=value.read(),filetype="pdf")
            if pdf.page_count==0:
                pdf.close()
                raise serializers.ValidationError("No page found")
            text=""
            for page in pdf:
                text+=page.get_text()
            pdf.close()
            if not text.strip():
                raise serializers.ValidationError("Pdf does not readable text")
            value.seek(0)
        except serializers.ValidationError:
            raise
        except Exception:
            raise serializers.ValidationError("Uploaded pdf is corrupt")
        return value

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=Skill
        fields=[
            "id",
            "name",
            "normalized_name",
        ]