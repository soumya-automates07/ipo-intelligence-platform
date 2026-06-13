import subprocess
import sys

from database.connection import engine
from database.models import PipelineRun
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

scripts = [
    "data_collectors/openai_blog.py",
    "data_collectors/anthropic_news.py",
    "data_collectors/spacex_news.py",
    "save_events.py"
]

success = True

articles_processed = 0
events_created = 0

for script in scripts:

    print(f"\nRunning {script}")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        success = False
        print(result.stderr)

run_record = PipelineRun(
    status="Success" if success else "Failed",
    articles_processed=articles_processed,
    events_created=events_created
)

session.add(run_record)
print("Saving pipeline run to database...")
session.commit()
print("Pipeline run saved!")

print("\nPipeline Complete!")