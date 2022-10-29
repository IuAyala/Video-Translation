import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import math
from pydub import AudioSegment

MAX_TEXT_LENGTH = 3000  # Polly limitation
OUTPUT_FORMAT = "mp3"

ENGINE = "standard"  # missing neural argument


def concatenate_audio_files(file_paths, output_path):
    combined_sounds = AudioSegment.empty()

    for el in file_paths:
        combined_sounds += AudioSegment.from_mp3(el)

    combined_sounds.export(output_path, format=OUTPUT_FORMAT)


def aws_tts_simple(text_str, file_path, voice_id="Joanna", output_format="mp3"):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = boto3.Session(profile_name="adminuser")
    polly = boto3.client("polly")  # default user

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text_str, OutputFormat=output_format,
                                           VoiceId=voice_id, Engine=ENGINE)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        raise Exception("Polly: 'synthesize_speech' returned an error")

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = file_path

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                raise Exception(
                    "Polly: Error while writing the output of the stream")

    else:
        # The response didn't contain audio data, exit gracefully
        print("Polly: Could not stream audio")
        raise Exception("Polly: Could not stream audio")


def aws_tts(text_str, file_path, voice_id="Joanna", output_format="mp3"):
    if len(text_str) >= MAX_TEXT_LENGTH:
        n_splits = math.ceil(len(text_str) / MAX_TEXT_LENGTH)

        file_temp_paths = []
        for i in range(n_splits):
            file_temp_path = file_path[:-4] + \
                "_temp_" + str(i) + file_path[-4:]
            file_temp_paths.append(file_temp_path)

            text_temp = text_str[i * MAX_TEXT_LENGTH:(i + 1) * MAX_TEXT_LENGTH]

            aws_tts_simple(text_temp, file_temp_path,
                           voice_id=voice_id, output_format=output_format)

        # Join audio files
        concatenate_audio_files(file_temp_paths, file_path)

    else:
        aws_tts_simple(text_str, file_path, voice_id=voice_id,
                       output_format=output_format)


if __name__ == "__main__":
    from tempfile import gettempdir

    # Parameters
    text = "This is a sample text to be converted to mp3 format"
    file_path = os.path.join(gettempdir(), "test_file.mp3")

    print("Generated in:", file_path)

    aws_tts(text, file_path)



