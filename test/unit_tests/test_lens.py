from dataclasses import dataclass
from uuid import UUID, uuid4

from lenses.key_lens import KeyLens


def test_nullable_lens():
    """
    Before:

    result = data(data["x"]["y"]).get("z", None)

    """

    data = {"x": {"y": None}}

    lens_x = KeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, dict | None](key="y")
    lens_z = KeyLens[dict, int](key="z")

    lens = lens_x | lens_y | lens_z

    error, result = lens(data)

    assert not error
    assert result is None
#
#
# def test_nullable_in_list():
#     """
#     # Get all z values from a list of data with optional y values
#
#     data = {"x": [{"y": None}, {"y": {"z": 42}}]}
#
#     # Good old procedural approach
#
#     result = []
#     for x in data["x"]:
#         y = x["y"]
#         if y:
#             result.append(y["z"])
#         else:
#             result.append(None)
#
#
#     # With list comprehension
#
#     def get_z(x):
#         return y["x"] if (y := x["y"]) else None
#
#     result = [get_z(x) for x in data["x"]]
#
#     # With one-line list comprehension
#
#     result = [y["z"] if (y := x["y"]) else None for x in data["x"]]
#
#     """
#     data = {"x": [
#         {"y": None},
#         {
#             "y": {
#                 "z": 42
#             }
#         }
#     ]}
#
#     lens_x = Lens[dict, dict](key="x")
#     lens_y = Lens[dict, dict | None](key="y")
#     lens_z = Lens[dict, int](key="z")
#
#     lens = lens_x | lens_y | lens_z
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == [None, 42]
#
#


#
# def test_nested_list():
#     data = {"x": [[{"y": 13, "z": 14}]]}
#
#     lens_x = Lens[dict, dict](key="x")
#     lens_yz = Lens[dict, int](key="y") + Lens[dict, int](key="z")
#
#     lens = lens_x | lens_yz
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == [[(13, 14)]]
#
#
# def test_transformer_with_scalar():
#     data = {"x": 42}
#
#     lens_x = Lens[dict, int](key="x")
#     inc = Transformer[int, int](lambda x: x + 1)
#
#     lens = lens_x | inc
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == 43
#
#


#
#
# def test_transformer_with_tuple():
#     data = {"x": [[{"y": 13, "z": 14}]]}
#
#     lens_x = Lens[dict, dict](key="x")
#     lens_yz = Lens[dict, int](key="y") + Lens[dict, int](key="z")
#     transformer = Transformer[tuple[int, int], tuple[int, int]](lambda y, z: (y + 1, z + 1))
#
#     lens = lens_x | lens_yz | transformer
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == [[(14, 15)]]
#
#
# def test_with_classes():
#     @dataclass
#     class Foo2:
#         z: int
#
#     @dataclass
#     class Foo1:
#         y: Foo2
#
#     @dataclass
#     class Foo:
#         x: Foo1
#
#     foo = Foo(x=Foo1(y=Foo2(z=666)))
#
#     lens_x = Lens[Foo, Foo1](key="x")
#     lens_y = Lens[Foo1, Foo2](key="y")
#     lens_z = Lens[Foo2, int](key="z")
#
#     lens = lens_x | lens_y | lens_z
#
#     error, result = lens(foo)
#
#     assert not error
#     assert result == 666
#
#
# def test_with_tuple():
#     data = {"x": ({"y": 1}, {"y": 2}, {"y": 3})}
#
#     lens_x = Lens[dict, dict](key="x")
#     lens_y = Lens[dict, int](key="y")
#
#     lens = lens_x | lens_y
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == (1, 2, 3)
#
#
# def test_nested_tuple():
#     data = {"x": (({"y": 1}, {"y": 2}), ({"y": 3}))}
#
#     lens_x = Lens(key="x")
#     lens_y = Lens(key="y")
#
#     lens = lens_x | lens_y
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == ((1, 2), 3)
#
#
# def test_filter():
#     data = [
#         {
#             "contents": "contents 1",
#             "label": "foo"
#         },
#         {
#             "contents": "contents 2",
#             "label": "bar"
#         }
#     ]
#     label = "foo"
#
#     lens_contents = Lens[dict, str](key="contents")
#     lens_label = Lens[dict, str](key="label")
#
#     filter_label = IsEqualFilter[str](lens_label, label)
#     first_or_none = AllTransformer(lambda l: first(l, None))
#
#     lens = lens_contents | filter_label | first_or_none
#
#     error, result = lens(data)
#
#     assert not error
#     assert result == "contents 1"
#
#     # contents = (ci["contents"] for ci in customer_info if ci["label"] == label)
#     # return first(contents, None)
#
#
def test_network_dashboard():
    @dataclass
    class ServicePort:
        vlan:str
        subscription_id: UUID

    owner_subscription_id = uuid4()

    l2vpn = {
        "vc": {
            "esis": [
                {
                    "saps": [
                        {
                            "vlanrange": "13, 13",
                            "port": {
                                "owner_subscription_id": owner_subscription_id
                            }
                        }
                    ]
                }
            ]
        }
    }
    lens_esis = KeyLens[dict, dict](key="vc") | KeyLens[dict, str](key="esis")
    lens_saps = lens_esis | KeyLens(key="saps")
#
#     lens_sp = Lens[dict, str](key="vlanrange") + (Lens[dict, str](key="port") | Lens[dict, UUID](key="owner_subscription_id"))
#     transformer = Transformer(lambda vlan, subscription_id: ServicePort(vlan=vlan, subscription_id=subscription_id))
#
#     lens_sp_transformed = lens_sp | transformer
#
#     lens = lens_saps | lens_sp_transformed
#
#     error, result = lens(l2vpn)
#
#     assert not error
#     assert result == [[ServicePort(vlan="13, 13", subscription_id=owner_subscription_id)]]