# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ommon.proto\x12\rdcs.common.v0\"G\n\x08Position\x12\x0b\n\x03lat\x18\x01 \x01(\x01\x12\x0b\n\x03lon\x18\x02 \x01(\x01\x12\x0b\n\x03\x61lt\x18\x03 \x01(\x01\x12\t\n\x01u\x18\x04 \x01(\x01\x12\t\n\x01v\x18\x05 \x01(\x01\"6\n\rInputPosition\x12\x0b\n\x03lat\x18\x01 \x01(\x01\x12\x0b\n\x03lon\x18\x02 \x01(\x01\x12\x0b\n\x03\x61lt\x18\x03 \x01(\x01\"\x17\n\x07Unknown\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xdc\x02\n\x04Unit\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x63\x61llsign\x18\x03 \x01(\t\x12+\n\tcoalition\x18\x04 \x01(\x0e\x32\x18.dcs.common.v0.Coalition\x12\x0c\n\x04type\x18\x05 \x01(\t\x12)\n\x08position\x18\x06 \x01(\x0b\x32\x17.dcs.common.v0.Position\x12/\n\x0borientation\x18\x07 \x01(\x0b\x32\x1a.dcs.common.v0.Orientation\x12)\n\x08velocity\x18\x08 \x01(\x0b\x32\x17.dcs.common.v0.Velocity\x12\x18\n\x0bplayer_name\x18\t \x01(\tH\x00\x88\x01\x01\x12#\n\x05group\x18\n \x01(\x0b\x32\x14.dcs.common.v0.Group\x12\x17\n\x0fnumber_in_group\x18\x0b \x01(\rB\x0e\n\x0c_player_name\"~\n\x05Group\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12+\n\tcoalition\x18\x03 \x01(\x0e\x32\x18.dcs.common.v0.Coalition\x12.\n\x08\x63\x61tegory\x18\x04 \x01(\x0e\x32\x1c.dcs.common.v0.GroupCategory\"\xa9\x01\n\x06Weapon\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04type\x18\x02 \x01(\t\x12)\n\x08position\x18\x03 \x01(\x0b\x32\x17.dcs.common.v0.Position\x12/\n\x0borientation\x18\x04 \x01(\x0b\x32\x1a.dcs.common.v0.Orientation\x12)\n\x08velocity\x18\x05 \x01(\x0b\x32\x17.dcs.common.v0.Velocity\"\x88\x01\n\x06Static\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12+\n\tcoalition\x18\x04 \x01(\x0e\x32\x18.dcs.common.v0.Coalition\x12)\n\x08position\x18\x05 \x01(\x0b\x32\x17.dcs.common.v0.Position\"N\n\x07Scenery\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04type\x18\x02 \x01(\t\x12)\n\x08position\x18\x03 \x01(\x0b\x32\x17.dcs.common.v0.Position\"\xfa\x01\n\x07\x41irbase\x12&\n\x04unit\x18\x01 \x01(\x0b\x32\x13.dcs.common.v0.UnitH\x00\x88\x01\x01\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x63\x61llsign\x18\x03 \x01(\t\x12+\n\tcoalition\x18\x04 \x01(\x0e\x32\x18.dcs.common.v0.Coalition\x12)\n\x08position\x18\x06 \x01(\x0b\x32\x17.dcs.common.v0.Position\x12\x30\n\x08\x63\x61tegory\x18\x07 \x01(\x0e\x32\x1e.dcs.common.v0.AirbaseCategory\x12\x14\n\x0c\x64isplay_name\x18\x08 \x01(\tB\x07\n\x05_unit\"\x07\n\x05\x43\x61rgo\"\xb7\x02\n\tInitiator\x12)\n\x07unknown\x18\x01 \x01(\x0b\x32\x16.dcs.common.v0.UnknownH\x00\x12#\n\x04unit\x18\x02 \x01(\x0b\x32\x13.dcs.common.v0.UnitH\x00\x12\'\n\x06weapon\x18\x03 \x01(\x0b\x32\x15.dcs.common.v0.WeaponH\x00\x12\'\n\x06static\x18\x04 \x01(\x0b\x32\x15.dcs.common.v0.StaticH\x00\x12)\n\x07scenery\x18\x05 \x01(\x0b\x32\x16.dcs.common.v0.SceneryH\x00\x12)\n\x07\x61irbase\x18\x06 \x01(\x0b\x32\x16.dcs.common.v0.AirbaseH\x00\x12%\n\x05\x63\x61rgo\x18\x07 \x01(\x0b\x32\x14.dcs.common.v0.CargoH\x00\x42\x0b\n\tinitiator\"\xb1\x02\n\x06Target\x12)\n\x07unknown\x18\x01 \x01(\x0b\x32\x16.dcs.common.v0.UnknownH\x00\x12#\n\x04unit\x18\x02 \x01(\x0b\x32\x13.dcs.common.v0.UnitH\x00\x12\'\n\x06weapon\x18\x03 \x01(\x0b\x32\x15.dcs.common.v0.WeaponH\x00\x12\'\n\x06static\x18\x04 \x01(\x0b\x32\x15.dcs.common.v0.StaticH\x00\x12)\n\x07scenery\x18\x05 \x01(\x0b\x32\x16.dcs.common.v0.SceneryH\x00\x12)\n\x07\x61irbase\x18\x06 \x01(\x0b\x32\x16.dcs.common.v0.AirbaseH\x00\x12%\n\x05\x63\x61rgo\x18\x07 \x01(\x0b\x32\x14.dcs.common.v0.CargoH\x00\x42\x08\n\x06target\"\x8b\x02\n\tMarkPanel\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04time\x18\x02 \x01(\x01\x12+\n\tinitiator\x18\x03 \x01(\x0b\x32\x13.dcs.common.v0.UnitH\x00\x88\x01\x01\x12\x30\n\tcoalition\x18\x04 \x01(\x0e\x32\x18.dcs.common.v0.CoalitionH\x01\x88\x01\x01\x12\x15\n\x08group_id\x18\x05 \x01(\rH\x02\x88\x01\x01\x12\x11\n\x04text\x18\x06 \x01(\tH\x03\x88\x01\x01\x12)\n\x08position\x18\x07 \x01(\x0b\x32\x17.dcs.common.v0.PositionB\x0c\n\n_initiatorB\x0c\n\n_coalitionB\x0b\n\t_group_idB\x07\n\x05_text\")\n\x06Vector\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\x12\t\n\x01z\x18\x03 \x01(\x01\"\xb9\x01\n\x0bOrientation\x12\x0f\n\x07heading\x18\x01 \x01(\x01\x12\x0b\n\x03yaw\x18\x02 \x01(\x01\x12\r\n\x05pitch\x18\x03 \x01(\x01\x12\x0c\n\x04roll\x18\x04 \x01(\x01\x12&\n\x07\x66orward\x18\x05 \x01(\x0b\x32\x15.dcs.common.v0.Vector\x12$\n\x05right\x18\x06 \x01(\x0b\x32\x15.dcs.common.v0.Vector\x12!\n\x02up\x18\x07 \x01(\x0b\x32\x15.dcs.common.v0.Vector\"S\n\x08Velocity\x12\x0f\n\x07heading\x18\x01 \x01(\x01\x12\r\n\x05speed\x18\x02 \x01(\x01\x12\'\n\x08velocity\x18\x03 \x01(\x0b\x32\x15.dcs.common.v0.Vector\"\xba\x01\n\x07\x43ontact\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0f\n\x07visible\x18\x02 \x01(\x08\x12\x10\n\x08\x64istance\x18\x03 \x01(\x08\x12(\n\x06object\x18\x04 \x01(\x0b\x32\x16.dcs.common.v0.UnknownH\x00\x12#\n\x04unit\x18\x05 \x01(\x0b\x32\x13.dcs.common.v0.UnitH\x00\x12\'\n\x06weapon\x18\x06 \x01(\x0b\x32\x15.dcs.common.v0.WeaponH\x00\x42\x08\n\x06target*\xd5\x01\n\x0eObjectCategory\x12\x1f\n\x1bOBJECT_CATEGORY_UNSPECIFIED\x10\x00\x12\x18\n\x14OBJECT_CATEGORY_UNIT\x10\x01\x12\x1a\n\x16OBJECT_CATEGORY_WEAPON\x10\x02\x12\x1a\n\x16OBJECT_CATEGORY_STATIC\x10\x03\x12\x1b\n\x17OBJECT_CATEGORY_SCENERY\x10\x04\x12\x18\n\x14OBJECT_CATEGORY_BASE\x10\x05\x12\x19\n\x15OBJECT_CATEGORY_CARGO\x10\x06*\x8b\x01\n\x0f\x41irbaseCategory\x12 \n\x1c\x41IRBASE_CATEGORY_UNSPECIFIED\x10\x00\x12\x1d\n\x19\x41IRBASE_CATEGORY_AIRDROME\x10\x01\x12\x1c\n\x18\x41IRBASE_CATEGORY_HELIPAD\x10\x02\x12\x19\n\x15\x41IRBASE_CATEGORY_SHIP\x10\x03*\\\n\tCoalition\x12\x11\n\rCOALITION_ALL\x10\x00\x12\x15\n\x11\x43OALITION_NEUTRAL\x10\x01\x12\x11\n\rCOALITION_RED\x10\x02\x12\x12\n\x0e\x43OALITION_BLUE\x10\x03*\xd9\x0f\n\x07\x43ountry\x12\x17\n\x13\x43OUNTRY_UNSPECIFIED\x10\x00\x12\x12\n\x0e\x43OUNTRY_RUSSIA\x10\x01\x12\x13\n\x0f\x43OUNTRY_UKRAINE\x10\x02\x12$\n COUNTRY_UNITED_STATES_OF_AMERICA\x10\x03\x12\x12\n\x0e\x43OUNTRY_TURKEY\x10\x04\x12\x1a\n\x16\x43OUNTRY_UNITED_KINGDOM\x10\x05\x12\x12\n\x0e\x43OUNTRY_FRANCE\x10\x06\x12\x13\n\x0f\x43OUNTRY_GERMANY\x10\x07\x12\x16\n\x12\x43OUNTRY_AGGRESSORS\x10\x08\x12\x12\n\x0e\x43OUNTRY_CANADA\x10\t\x12\x11\n\rCOUNTRY_SPAIN\x10\n\x12\x1b\n\x17\x43OUNTRY_THE_NETHERLANDS\x10\x0b\x12\x13\n\x0f\x43OUNTRY_BELGIUM\x10\x0c\x12\x12\n\x0e\x43OUNTRY_NORWAY\x10\r\x12\x13\n\x0f\x43OUNTRY_DENMARK\x10\x0e\x12\x12\n\x0e\x43OUNTRY_UNUSED\x10\x0f\x12\x12\n\x0e\x43OUNTRY_ISRAEL\x10\x10\x12\x13\n\x0f\x43OUNTRY_GEORGIA\x10\x11\x12\x16\n\x12\x43OUNTRY_INSURGENTS\x10\x12\x12\x14\n\x10\x43OUNTRY_ABKHAZIA\x10\x13\x12\x18\n\x14\x43OUNTRY_SOUTH_OSETIA\x10\x14\x12\x11\n\rCOUNTRY_ITALY\x10\x15\x12\x15\n\x11\x43OUNTRY_AUSTRALIA\x10\x16\x12\x17\n\x13\x43OUNTRY_SWITZERLAND\x10\x17\x12\x13\n\x0f\x43OUNTRY_AUSTRIA\x10\x18\x12\x13\n\x0f\x43OUNTRY_BELARUS\x10\x19\x12\x14\n\x10\x43OUNTRY_BULGARIA\x10\x1a\x12\x1a\n\x16\x43OUNTRY_CZECH_REPUBLIC\x10\x1b\x12\x11\n\rCOUNTRY_CHINA\x10\x1c\x12\x13\n\x0f\x43OUNTRY_CROATIA\x10\x1d\x12\x11\n\rCOUNTRY_EGYPT\x10\x1e\x12\x13\n\x0f\x43OUNTRY_FINLAND\x10\x1f\x12\x12\n\x0e\x43OUNTRY_GREECE\x10 \x12\x13\n\x0f\x43OUNTRY_HUNGARY\x10!\x12\x11\n\rCOUNTRY_INDIA\x10\"\x12\x10\n\x0c\x43OUNTRY_IRAN\x10#\x12\x10\n\x0c\x43OUNTRY_IRAQ\x10$\x12\x11\n\rCOUNTRY_JAPAN\x10%\x12\x16\n\x12\x43OUNTRY_KAZAKHSTAN\x10&\x12\x17\n\x13\x43OUNTRY_NORTH_KOREA\x10\'\x12\x14\n\x10\x43OUNTRY_PAKISTAN\x10(\x12\x12\n\x0e\x43OUNTRY_POLAND\x10)\x12\x13\n\x0f\x43OUNTRY_ROMANIA\x10*\x12\x18\n\x14\x43OUNTRY_SAUDI_ARABIA\x10+\x12\x12\n\x0e\x43OUNTRY_SERBIA\x10,\x12\x14\n\x10\x43OUNTRY_SLOVAKIA\x10-\x12\x17\n\x13\x43OUNTRY_SOUTH_KOREA\x10.\x12\x12\n\x0e\x43OUNTRY_SWEDEN\x10/\x12\x11\n\rCOUNTRY_SYRIA\x10\x30\x12\x11\n\rCOUNTRY_YEMEN\x10\x31\x12\x13\n\x0f\x43OUNTRY_VIETNAM\x10\x32\x12\x15\n\x11\x43OUNTRY_VENEZUELA\x10\x33\x12\x13\n\x0f\x43OUNTRY_TUNISIA\x10\x34\x12\x14\n\x10\x43OUNTRY_THAILAND\x10\x35\x12\x11\n\rCOUNTRY_SUDAN\x10\x36\x12\x17\n\x13\x43OUNTRY_PHILIPPINES\x10\x37\x12\x13\n\x0f\x43OUNTRY_MOROCCO\x10\x38\x12\x12\n\x0e\x43OUNTRY_MEXICO\x10\x39\x12\x14\n\x10\x43OUNTRY_MALAYSIA\x10:\x12\x11\n\rCOUNTRY_LIBYA\x10;\x12\x12\n\x0e\x43OUNTRY_JORDAN\x10<\x12\x15\n\x11\x43OUNTRY_INDONESIA\x10=\x12\x14\n\x10\x43OUNTRY_HONDURAS\x10>\x12\x14\n\x10\x43OUNTRY_ETHIOPIA\x10?\x12\x11\n\rCOUNTRY_CHILE\x10@\x12\x12\n\x0e\x43OUNTRY_BRAZIL\x10\x41\x12\x13\n\x0f\x43OUNTRY_BAHRAIN\x10\x42\x12\x16\n\x12\x43OUNTRY_THIRDREICH\x10\x43\x12\x16\n\x12\x43OUNTRY_YUGOSLAVIA\x10\x44\x12\x18\n\x14\x43OUNTRY_SOVIET_UNION\x10\x45\x12#\n\x1f\x43OUNTRY_ITALIAN_SOCIAL_REPUBLIC\x10\x46\x12\x13\n\x0f\x43OUNTRY_ALGERIA\x10G\x12\x12\n\x0e\x43OUNTRY_KUWAIT\x10H\x12\x11\n\rCOUNTRY_QATAR\x10I\x12\x10\n\x0c\x43OUNTRY_OMAN\x10J\x12 \n\x1c\x43OUNTRY_UNITED_ARAB_EMIRATES\x10K\x12\x18\n\x14\x43OUNTRY_SOUTH_AFRICA\x10L\x12\x10\n\x0c\x43OUNTRY_CUBA\x10M\x12\x14\n\x10\x43OUNTRY_PORTUGAL\x10N\x12&\n\"COUNTRY_GERMAN_DEMOCRATIC_REPUBLIC\x10O\x12\x13\n\x0f\x43OUNTRY_LEBANON\x10P\x12*\n&COUNTRY_COMBINED_JOINT_TASK_FORCE_BLUE\x10Q\x12)\n%COUNTRY_COMBINED_JOINT_TASK_FORCE_RED\x10R\x12\'\n#COUNTRY_UNITED_NATIONS_PEACEKEEPERS\x10S\x12\x15\n\x11\x43OUNTRY_ARGENTINA\x10T\x12\x12\n\x0e\x43OUNTRY_CYPRUS\x10U\x12\x14\n\x10\x43OUNTRY_SLOVENIA\x10V*\xb9\x01\n\rGroupCategory\x12\x1e\n\x1aGROUP_CATEGORY_UNSPECIFIED\x10\x00\x12\x1b\n\x17GROUP_CATEGORY_AIRPLANE\x10\x01\x12\x1d\n\x19GROUP_CATEGORY_HELICOPTER\x10\x02\x12\x19\n\x15GROUP_CATEGORY_GROUND\x10\x03\x12\x17\n\x13GROUP_CATEGORY_SHIP\x10\x04\x12\x18\n\x14GROUP_CATEGORY_TRAIN\x10\x05\x42QZ-github.com/DCS-gRPC/go-bindings/dcs/v0/common\xaa\x02\x1fRurouniJones.Dcs.Grpc.V0.Commonb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/DCS-gRPC/go-bindings/dcs/v0/common\252\002\037RurouniJones.Dcs.Grpc.V0.Common'
  _OBJECTCATEGORY._serialized_start=2715
  _OBJECTCATEGORY._serialized_end=2928
  _AIRBASECATEGORY._serialized_start=2931
  _AIRBASECATEGORY._serialized_end=3070
  _COALITION._serialized_start=3072
  _COALITION._serialized_end=3164
  _COUNTRY._serialized_start=3167
  _COUNTRY._serialized_end=5176
  _GROUPCATEGORY._serialized_start=5179
  _GROUPCATEGORY._serialized_end=5364
  _POSITION._serialized_start=31
  _POSITION._serialized_end=102
  _INPUTPOSITION._serialized_start=104
  _INPUTPOSITION._serialized_end=158
  _UNKNOWN._serialized_start=160
  _UNKNOWN._serialized_end=183
  _UNIT._serialized_start=186
  _UNIT._serialized_end=534
  _GROUP._serialized_start=536
  _GROUP._serialized_end=662
  _WEAPON._serialized_start=665
  _WEAPON._serialized_end=834
  _STATIC._serialized_start=837
  _STATIC._serialized_end=973
  _SCENERY._serialized_start=975
  _SCENERY._serialized_end=1053
  _AIRBASE._serialized_start=1056
  _AIRBASE._serialized_end=1306
  _CARGO._serialized_start=1308
  _CARGO._serialized_end=1315
  _INITIATOR._serialized_start=1318
  _INITIATOR._serialized_end=1629
  _TARGET._serialized_start=1632
  _TARGET._serialized_end=1937
  _MARKPANEL._serialized_start=1940
  _MARKPANEL._serialized_end=2207
  _VECTOR._serialized_start=2209
  _VECTOR._serialized_end=2250
  _ORIENTATION._serialized_start=2253
  _ORIENTATION._serialized_end=2438
  _VELOCITY._serialized_start=2440
  _VELOCITY._serialized_end=2523
  _CONTACT._serialized_start=2526
  _CONTACT._serialized_end=2712
# @@protoc_insertion_point(module_scope)
