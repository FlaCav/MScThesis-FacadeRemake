from elevenlabs.client import ElevenLabs
from elevenlabs import save

client = ElevenLabs(
  api_key="ELEVEN_API_KEY", # Defaults to ELEVEN_API_KEY
)

voice = client.clone(
    name="Grace",
    description="The female voice from Facade, bright and pleasant.", # Optional
    files=["C:\\Users\\Admin\\Downloads\\t-files1.mp3", "C:\\Users\\Admin\\Downloads\\t-files2.mp3",
           "C:\\Users\\Admin\\Downloads\\t-files3.mp3", "C:\\Users\\Admin\\Downloads\\t-files4.mp3", "C:\\Users\\Admin\\Downloads\\t-files5.mp3",
           "C:\\Users\\Admin\\Downloads\\t-files6.mp3", "C:\\Users\\Admin\\Downloads\\t-files7.mp3",
           "C:\\Users\\Admin\\Downloads\\t-files8.mp3"],
)

print("*** The generated voice: ***")
print(voice)

audio = client.generate(text="Hi! I'm a cloned voice! I travel to Europe a lot for business, at least that's what I tell my wife. If you don't lke my fancy drinks, then IT'S TIME FOR YOU TO LEAVE. Whoop dee doo!!", voice=voice)

#play(audio)
# saves audio to file
save(audio, "trip-sample-file.mp3")


"""
Grace:
files=["C:\\Users\\Admin\\Downloads\\g-file1.mp3", "C:\\Users\\Admin\\Downloads\\g-file2.mp3", "C:\\Users\\Admin\\Downloads\\g-file3.mp3",
           "C:\\Users\\Admin\\Downloads\\g-file4.mp3", "C:\\Users\\Admin\\Downloads\\g-file5.mp3", "C:\\Users\\Admin\\Downloads\\g-file6.mp3",
           "C:\\Users\\Admin\\Downloads\\g-file7.mp3", "C:\\Users\\Admin\\Downloads\\g-file8.mp3", "C:\\Users\\Admin\\Downloads\\g-file9.mp3",
           "C:\\Users\\Admin\\Downloads\\g-file10.mp3", "C:\\Users\\Admin\\Downloads\\g-file11.mp3", "C:\\Users\\Admin\\Downloads\\g-file12.mp3",
           "C:\\Users\\Admin\\Downloads\\g-file13.mp3"]
"""