# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: custom.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ustom.proto\x12\rdcs.custom.v0\"J\n\x1fRequestMissionAssignmentRequest\x12\x11\n\tunit_name\x18\x01 \x01(\t\x12\x14\n\x0cmission_type\x18\x02 \x01(\t\"\"\n RequestMissionAssignmentResponse\"=\n\x12JoinMissionRequest\x12\x11\n\tunit_name\x18\x01 \x01(\t\x12\x14\n\x0cmission_code\x18\x02 \x01(\x05\"\x15\n\x13JoinMissionResponse\"(\n\x13\x41\x62ortMissionRequest\x12\x11\n\tunit_name\x18\x01 \x01(\t\"\x16\n\x14\x41\x62ortMissionResponse\",\n\x17GetMissionStatusRequest\x12\x11\n\tunit_name\x18\x01 \x01(\t\"\x1a\n\x18GetMissionStatusResponse\"\x1a\n\x0b\x45valRequest\x12\x0b\n\x03lua\x18\x01 \x01(\t\"\x1c\n\x0c\x45valResponse\x12\x0c\n\x04json\x18\x01 \x01(\t\"F\n\x1dGetMagneticDeclinationRequest\x12\x0b\n\x03lat\x18\x01 \x01(\x01\x12\x0b\n\x03lon\x18\x02 \x01(\x01\x12\x0b\n\x03\x61lt\x18\x03 \x01(\x01\"5\n\x1eGetMagneticDeclinationResponse\x12\x13\n\x0b\x64\x65\x63lination\x18\x01 \x01(\x01\x32\xe4\x04\n\rCustomService\x12}\n\x18RequestMissionAssignment\x12..dcs.custom.v0.RequestMissionAssignmentRequest\x1a/.dcs.custom.v0.RequestMissionAssignmentResponse\"\x00\x12V\n\x0bJoinMission\x12!.dcs.custom.v0.JoinMissionRequest\x1a\".dcs.custom.v0.JoinMissionResponse\"\x00\x12Y\n\x0c\x41\x62ortMission\x12\".dcs.custom.v0.AbortMissionRequest\x1a#.dcs.custom.v0.AbortMissionResponse\"\x00\x12\x65\n\x10GetMissionStatus\x12&.dcs.custom.v0.GetMissionStatusRequest\x1a\'.dcs.custom.v0.GetMissionStatusResponse\"\x00\x12\x41\n\x04\x45val\x12\x1a.dcs.custom.v0.EvalRequest\x1a\x1b.dcs.custom.v0.EvalResponse\"\x00\x12w\n\x16GetMagneticDeclination\x12,.dcs.custom.v0.GetMagneticDeclinationRequest\x1a-.dcs.custom.v0.GetMagneticDeclinationResponse\"\x00\x42QZ-github.com/DCS-gRPC/go-bindings/dcs/v0/custom\xaa\x02\x1fRurouniJones.Dcs.Grpc.V0.Customb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'custom_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/DCS-gRPC/go-bindings/dcs/v0/custom\252\002\037RurouniJones.Dcs.Grpc.V0.Custom'
  _REQUESTMISSIONASSIGNMENTREQUEST._serialized_start=31
  _REQUESTMISSIONASSIGNMENTREQUEST._serialized_end=105
  _REQUESTMISSIONASSIGNMENTRESPONSE._serialized_start=107
  _REQUESTMISSIONASSIGNMENTRESPONSE._serialized_end=141
  _JOINMISSIONREQUEST._serialized_start=143
  _JOINMISSIONREQUEST._serialized_end=204
  _JOINMISSIONRESPONSE._serialized_start=206
  _JOINMISSIONRESPONSE._serialized_end=227
  _ABORTMISSIONREQUEST._serialized_start=229
  _ABORTMISSIONREQUEST._serialized_end=269
  _ABORTMISSIONRESPONSE._serialized_start=271
  _ABORTMISSIONRESPONSE._serialized_end=293
  _GETMISSIONSTATUSREQUEST._serialized_start=295
  _GETMISSIONSTATUSREQUEST._serialized_end=339
  _GETMISSIONSTATUSRESPONSE._serialized_start=341
  _GETMISSIONSTATUSRESPONSE._serialized_end=367
  _EVALREQUEST._serialized_start=369
  _EVALREQUEST._serialized_end=395
  _EVALRESPONSE._serialized_start=397
  _EVALRESPONSE._serialized_end=425
  _GETMAGNETICDECLINATIONREQUEST._serialized_start=427
  _GETMAGNETICDECLINATIONREQUEST._serialized_end=497
  _GETMAGNETICDECLINATIONRESPONSE._serialized_start=499
  _GETMAGNETICDECLINATIONRESPONSE._serialized_end=552
  _CUSTOMSERVICE._serialized_start=555
  _CUSTOMSERVICE._serialized_end=1167
# @@protoc_insertion_point(module_scope)
