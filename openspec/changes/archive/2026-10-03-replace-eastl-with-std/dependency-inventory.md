# Dependency inventory

Captured from tracked files in the four consumer repositories before implementation. `dependency-inventory.json` records paths, include names, and symbol counts. Bundled EASTL/EABase implementation trees are excluded; other bundled integration and inactive/commented uses are included. This is a lexical inventory, not a compiled-target reachability claim.

## Symbol replacements

Every observed symbol has a proposed destination below. Standard-name matches still require API/overload and behavior review; they do not authorize mechanical substitution.

| Symbol | Occurrences | Destination / contract |
| --- | ---: | --- |
| `BitvectorWordType` | 1 | Explicit word type preserving bit layout |
| `CharStrlen` | 13 | std::char_traits<Char>::length |
| `GetDefaultAllocator` | 1 | Nau owning default resource |
| `accumulate` | 17 | Toolchain `std::accumulate`; review signatures, allocation and semantics at call sites |
| `add_lvalue_reference_t` | 1 | Toolchain `std::add_lvalue_reference_t`; review signatures, allocation and semantics at call sites |
| `add_pointer` | 24 | Toolchain `std::add_pointer`; review signatures, allocation and semantics at call sites |
| `add_pointer_t` | 6 | Toolchain `std::add_pointer_t`; review signatures, allocation and semantics at call sites |
| `addressof` | 7 | Toolchain `std::addressof`; review signatures, allocation and semantics at call sites |
| `advance` | 1 | Toolchain `std::advance`; review signatures, allocation and semantics at call sites |
| `aligned_storage` | 1 | Toolchain `std::aligned_storage`; review signatures, allocation and semantics at call sites |
| `all_of` | 11 | Toolchain `std::all_of`; review signatures, allocation and semantics at call sites |
| `allocate_memory` | 5 | Nau checked aligned allocation |
| `allocator` | 61 | Typed Nau resource adapter |
| `allocators` | 1 | Allocator integration; classify definition context |
| `any_of` | 12 | Toolchain `std::any_of`; review signatures, allocation and semantics at call sites |
| `apply` | 3 | Toolchain `std::apply`; review signatures, allocation and semantics at call sites |
| `array` | 74 | Toolchain `std::array`; review signatures, allocation and semantics at call sites |
| `atomic` | 3 | Toolchain `std::atomic`; review signatures, allocation and semantics at call sites |
| `back_insert_iterator` | 2 | Toolchain `std::back_insert_iterator`; review signatures, allocation and semantics at call sites |
| `back_inserter` | 8 | Toolchain `std::back_inserter`; review signatures, allocation and semantics at call sites |
| `basic_string` | 17 | Toolchain `std::basic_string`; review signatures, allocation and semantics at call sites |
| `basic_string_view` | 17 | Toolchain `std::basic_string_view`; review signatures, allocation and semantics at call sites |
| `begin` | 87 | Toolchain `std::begin`; review signatures, allocation and semantics at call sites |
| `bidirectional_iterator_tag` | 1 | Toolchain `std::bidirectional_iterator_tag`; review signatures, allocation and semantics at call sites |
| `binary_function` | 2 | Remove obsolete base; retain required aliases explicitly |
| `binary_search` | 5 | Toolchain `std::binary_search`; review signatures, allocation and semantics at call sites |
| `binary_search_i` | 2 | std::lower_bound plus equality; preserve iterator result |
| `bit_cast` | 1 | Toolchain `std::bit_cast`; review signatures, allocation and semantics at call sites |
| `bitset` | 38 | Toolchain `std::bitset`; review signatures, allocation and semantics at call sites |
| `bitvector` | 23 | Nau dynamic word-backed bits; resize/tail masking |
| `chrono` | 16 | Toolchain `std::chrono`; review signatures, allocation and semantics at call sites |
| `chrono_literals` | 4 | Toolchain `std::chrono_literals`; review signatures, allocation and semantics at call sites |
| `clamp` | 10 | Toolchain `std::clamp`; review signatures, allocation and semantics at call sites |
| `compressed_pair` | 3 | Nau pair with no_unique_address where needed; check layout assumptions |
| `conditional` | 5 | Toolchain `std::conditional`; review signatures, allocation and semantics at call sites |
| `conditional_t` | 12 | Toolchain `std::conditional_t`; review signatures, allocation and semantics at call sites |
| `copy` | 45 | Toolchain `std::copy`; review signatures, allocation and semantics at call sites |
| `copy_backward` | 1 | Toolchain `std::copy_backward`; review signatures, allocation and semantics at call sites |
| `copy_n` | 10 | Toolchain `std::copy_n`; review signatures, allocation and semantics at call sites |
| `decay` | 27 | Toolchain `std::decay`; review signatures, allocation and semantics at call sites |
| `decay_t` | 4 | Toolchain `std::decay_t`; review signatures, allocation and semantics at call sites |
| `declval` | 39 | Toolchain `std::declval`; review signatures, allocation and semantics at call sites |
| `deque` | 4 | Toolchain `std::deque`; review signatures, allocation and semantics at call sites |
| `destroy_at` | 6 | Toolchain `std::destroy_at`; review signatures, allocation and semantics at call sites |
| `destruct` | 18 | std::destroy_at/destroy after checking argument range |
| `disable_if` | 10 | std::enable_if with negated predicate |
| `disable_if_t` | 5 | std::enable_if_t with negated predicate |
| `disjunction` | 1 | Toolchain `std::disjunction`; review signatures, allocation and semantics at call sites |
| `distance` | 39 | Toolchain `std::distance`; review signatures, allocation and semantics at call sites |
| `dynamic_extent` | 2 | Toolchain `std::dynamic_extent`; review signatures, allocation and semantics at call sites |
| `enable_if` | 48 | Toolchain `std::enable_if`; review signatures, allocation and semantics at call sites |
| `enable_if_t` | 27 | Toolchain `std::enable_if_t`; review signatures, allocation and semantics at call sites |
| `enable_shared_from_this` | 1 | Toolchain `std::enable_shared_from_this`; review signatures, allocation and semantics at call sites |
| `end` | 95 | Toolchain `std::end`; review signatures, allocation and semantics at call sites |
| `equal` | 16 | Toolchain `std::equal`; review signatures, allocation and semantics at call sites |
| `equal_to` | 8 | Toolchain `std::equal_to`; review signatures, allocation and semantics at call sites |
| `equal_to_2` | 2 | std::equal_to<>; validate heterogeneous equality |
| `erase` | 2 | Toolchain `std::erase`; review signatures, allocation and semantics at call sites |
| `erase_if` | 12 | Toolchain `std::erase_if`; review signatures, allocation and semantics at call sites |
| `exchange` | 11 | Toolchain `std::exchange`; review signatures, allocation and semantics at call sites |
| `extent` | 3 | Toolchain `std::extent`; review signatures, allocation and semantics at call sites |
| `false_type` | 13 | Toolchain `std::false_type`; review signatures, allocation and semantics at call sites |
| `fill` | 13 | Toolchain `std::fill`; review signatures, allocation and semantics at call sites |
| `fill_n` | 9 | Toolchain `std::fill_n`; review signatures, allocation and semantics at call sites |
| `find` | 43 | Toolchain `std::find`; review signatures, allocation and semantics at call sites |
| `find_if` | 133 | Toolchain `std::find_if`; review signatures, allocation and semantics at call sites |
| `find_if_not` | 3 | Toolchain `std::find_if_not`; review signatures, allocation and semantics at call sites |
| `find_last_of` | 1 | Reverse search adapter preserving returned index/iterator |
| `fixed_function` | 12 | DESIGN GAP: fixed-size callable storage, copy semantics and no heap spill |
| `fixed_map` | 8 | DESIGN GAP: inline node pool, ordering, overflow and reference stability |
| `fixed_string` | 9 | Nau inline string; preserve terminator/capacity/overflow |
| `fixed_vector` | 29 | Nau inline vector; preserve capacity, allocator and overflow policy |
| `fixed_vector_allocator` | 1 | Nau inline-storage implementation; preserve overflow resource |
| `for_each` | 2 | Toolchain `std::for_each`; review signatures, allocation and semantics at call sites |
| `forward` | 123 | Toolchain `std::forward`; review signatures, allocation and semantics at call sites |
| `forward_iterator_tag` | 1 | Toolchain `std::forward_iterator_tag`; review signatures, allocation and semantics at call sites |
| `function` | 56 | Toolchain `std::function`; review signatures, allocation and semantics at call sites |
| `get` | 73 | Toolchain `std::get`; review signatures, allocation and semantics at call sites |
| `get_if` | 44 | Toolchain `std::get_if`; review signatures, allocation and semantics at call sites |
| `greater` | 2 | Toolchain `std::greater`; review signatures, allocation and semantics at call sites |
| `has_equality` | 1 | C++20 requires expression |
| `hash` | 38 | std::hash for transient lookup only; preserve explicit persistent algorithms |
| `hash_map` | 8 | std::unordered_map; explicit compatible hash/equality |
| `hash_set` | 4 | std::unordered_set; explicit compatible hash/equality |
| `holds_alternative` | 45 | Toolchain `std::holds_alternative`; review signatures, allocation and semantics at call sites |
| `in_place` | 2 | Toolchain `std::in_place`; review signatures, allocation and semantics at call sites |
| `input_iterator_tag` | 3 | Toolchain `std::input_iterator_tag`; review signatures, allocation and semantics at call sites |
| `inserter` | 2 | Toolchain `std::inserter`; review signatures, allocation and semantics at call sites |
| `integral_constant` | 7 | Toolchain `std::integral_constant`; review signatures, allocation and semantics at call sites |
| `intrusive_list` | 5 | Nau non-owning list; identity and unlink lifetime |
| `intrusive_list_node` | 5 | Nau non-owning node links |
| `intrusive_ptr` | 2 | DESIGN GAP: external add-ref/release ownership; do not replace with shared_ptr control blocks |
| `intrusive_ptr_add_ref` | 1 | DESIGN GAP: retain intrusive reference-count hook contract |
| `intrusive_ptr_release` | 1 | DESIGN GAP: retain intrusive reference-count hook contract |
| `invoke` | 2 | Toolchain `std::invoke`; review signatures, allocation and semantics at call sites |
| `invoke_result_t` | 4 | Toolchain `std::invoke_result_t`; review signatures, allocation and semantics at call sites |
| `iota` | 6 | Toolchain `std::iota`; review signatures, allocation and semantics at call sites |
| `is_aggregate_v` | 1 | Toolchain `std::is_aggregate_v`; review signatures, allocation and semantics at call sites |
| `is_arithmetic` | 1 | Toolchain `std::is_arithmetic`; review signatures, allocation and semantics at call sites |
| `is_base_of` | 3 | Toolchain `std::is_base_of`; review signatures, allocation and semantics at call sites |
| `is_base_of_v` | 8 | Toolchain `std::is_base_of_v`; review signatures, allocation and semantics at call sites |
| `is_const` | 1 | Toolchain `std::is_const`; review signatures, allocation and semantics at call sites |
| `is_const_v` | 9 | Toolchain `std::is_const_v`; review signatures, allocation and semantics at call sites |
| `is_constructible` | 4 | Toolchain `std::is_constructible`; review signatures, allocation and semantics at call sites |
| `is_convertible` | 11 | Toolchain `std::is_convertible`; review signatures, allocation and semantics at call sites |
| `is_copy_assignable` | 3 | Toolchain `std::is_copy_assignable`; review signatures, allocation and semantics at call sites |
| `is_copy_constructible` | 4 | Toolchain `std::is_copy_constructible`; review signatures, allocation and semantics at call sites |
| `is_default_constructible` | 1 | Toolchain `std::is_default_constructible`; review signatures, allocation and semantics at call sites |
| `is_enum` | 1 | Toolchain `std::is_enum`; review signatures, allocation and semantics at call sites |
| `is_enum_v` | 3 | Toolchain `std::is_enum_v`; review signatures, allocation and semantics at call sites |
| `is_integral` | 5 | Toolchain `std::is_integral`; review signatures, allocation and semantics at call sites |
| `is_invocable_v` | 4 | Toolchain `std::is_invocable_v`; review signatures, allocation and semantics at call sites |
| `is_lvalue_reference_v` | 1 | Toolchain `std::is_lvalue_reference_v`; review signatures, allocation and semantics at call sites |
| `is_move_assignable` | 2 | Toolchain `std::is_move_assignable`; review signatures, allocation and semantics at call sites |
| `is_move_constructible` | 2 | Toolchain `std::is_move_constructible`; review signatures, allocation and semantics at call sites |
| `is_pointer` | 5 | Toolchain `std::is_pointer`; review signatures, allocation and semantics at call sites |
| `is_rvalue_reference` | 14 | Toolchain `std::is_rvalue_reference`; review signatures, allocation and semantics at call sites |
| `is_same` | 13 | Toolchain `std::is_same`; review signatures, allocation and semantics at call sites |
| `is_same_v` | 14 | Toolchain `std::is_same_v`; review signatures, allocation and semantics at call sites |
| `is_scalar` | 8 | Toolchain `std::is_scalar`; review signatures, allocation and semantics at call sites |
| `is_signed` | 2 | Toolchain `std::is_signed`; review signatures, allocation and semantics at call sites |
| `is_sorted` | 2 | Toolchain `std::is_sorted`; review signatures, allocation and semantics at call sites |
| `is_trivially_copy_assignable_v` | 3 | Toolchain `std::is_trivially_copy_assignable_v`; review signatures, allocation and semantics at call sites |
| `is_trivially_copy_constructible` | 6 | Toolchain `std::is_trivially_copy_constructible`; review signatures, allocation and semantics at call sites |
| `is_trivially_copyable_v` | 2 | Toolchain `std::is_trivially_copyable_v`; review signatures, allocation and semantics at call sites |
| `is_trivially_default_constructible` | 1 | Toolchain `std::is_trivially_default_constructible`; review signatures, allocation and semantics at call sites |
| `is_trivially_destructible` | 10 | Toolchain `std::is_trivially_destructible`; review signatures, allocation and semantics at call sites |
| `is_trivially_move_assignable` | 7 | Toolchain `std::is_trivially_move_assignable`; review signatures, allocation and semantics at call sites |
| `is_trivially_move_constructible` | 6 | Toolchain `std::is_trivially_move_constructible`; review signatures, allocation and semantics at call sites |
| `is_unsigned` | 2 | Toolchain `std::is_unsigned`; review signatures, allocation and semantics at call sites |
| `is_unsigned_v` | 2 | Toolchain `std::is_unsigned_v`; review signatures, allocation and semantics at call sites |
| `is_void_v` | 1 | Toolchain `std::is_void_v`; review signatures, allocation and semantics at call sites |
| `isf_valid` | 1 | Context-specific trait; review use before standard replacement |
| `iter_swap` | 21 | Toolchain `std::iter_swap`; review signatures, allocation and semantics at call sites |
| `iterator_traits` | 21 | Toolchain `std::iterator_traits`; review signatures, allocation and semantics at call sites |
| `less` | 27 | Toolchain `std::less`; review signatures, allocation and semantics at call sites |
| `less_2` | 6 | std::less<>; validate heterogeneous comparison |
| `list` | 34 | Toolchain `std::list`; review signatures, allocation and semantics at call sites |
| `lower_bound` | 26 | Toolchain `std::lower_bound`; review signatures, allocation and semantics at call sites |
| `lru_cache` | 1 | DESIGN GAP: preserve recency updates, capacity and eviction lifetime |
| `make_heap` | 1 | Toolchain `std::make_heap`; review signatures, allocation and semantics at call sites |
| `make_optional` | 5 | Toolchain `std::make_optional`; review signatures, allocation and semantics at call sites |
| `make_pair` | 7 | Toolchain `std::make_pair`; review signatures, allocation and semantics at call sites |
| `make_reverse_iterator` | 1 | Toolchain `std::make_reverse_iterator`; review signatures, allocation and semantics at call sites |
| `make_shared` | 55 | Toolchain `std::make_shared`; review signatures, allocation and semantics at call sites |
| `make_signed` | 2 | Toolchain `std::make_signed`; review signatures, allocation and semantics at call sites |
| `make_signed_t` | 1 | Toolchain `std::make_signed_t`; review signatures, allocation and semantics at call sites |
| `make_tuple` | 7 | Toolchain `std::make_tuple`; review signatures, allocation and semantics at call sites |
| `make_unique` | 244 | Toolchain `std::make_unique`; review signatures, allocation and semantics at call sites |
| `make_unsigned` | 3 | Toolchain `std::make_unsigned`; review signatures, allocation and semantics at call sites |
| `map` | 52 | Toolchain `std::map`; review signatures, allocation and semantics at call sites |
| `max` | 91 | Toolchain `std::max`; review signatures, allocation and semantics at call sites |
| `max_alt` | 3 | std::max with macro-safe call |
| `max_element` | 11 | Toolchain `std::max_element`; review signatures, allocation and semantics at call sites |
| `memory_order_relaxed` | 3 | Toolchain `std::memory_order_relaxed`; review signatures, allocation and semantics at call sites |
| `min` | 66 | Toolchain `std::min`; review signatures, allocation and semantics at call sites |
| `min_alt` | 10 | std::min with macro-safe call |
| `min_element` | 5 | Toolchain `std::min_element`; review signatures, allocation and semantics at call sites |
| `mismatch` | 1 | Toolchain `std::mismatch`; review signatures, allocation and semantics at call sites |
| `monostate` | 21 | Toolchain `std::monostate`; review signatures, allocation and semantics at call sites |
| `move` | 570 | Toolchain `std::move`; review signatures, allocation and semantics at call sites |
| `move_backward` | 4 | Toolchain `std::move_backward`; review signatures, allocation and semantics at call sites |
| `move_iterator` | 6 | Toolchain `std::move_iterator`; review signatures, allocation and semantics at call sites |
| `multimap` | 2 | Toolchain `std::multimap`; review signatures, allocation and semantics at call sites |
| `multiset` | 1 | Toolchain `std::multiset`; review signatures, allocation and semantics at call sites |
| `next` | 2 | Toolchain `std::next`; review signatures, allocation and semantics at call sites |
| `no_type` | 7 | Replace detection helper with std::false_type; review sizeof-based consumers |
| `nullopt` | 86 | Toolchain `std::nullopt`; review signatures, allocation and semantics at call sites |
| `numeric_limits` | 94 | Toolchain `std::numeric_limits`; review signatures, allocation and semantics at call sites |
| `optional` | 174 | Toolchain `std::optional`; review signatures, allocation and semantics at call sites |
| `pair` | 135 | Toolchain `std::pair`; review signatures, allocation and semantics at call sites |
| `partial_sum` | 5 | Toolchain `std::partial_sum`; review signatures, allocation and semantics at call sites |
| `partition` | 4 | Toolchain `std::partition`; review signatures, allocation and semantics at call sites |
| `pointer_traits` | 2 | Toolchain `std::pointer_traits`; review signatures, allocation and semantics at call sites |
| `prev` | 3 | Toolchain `std::prev`; review signatures, allocation and semantics at call sites |
| `priority_queue` | 1 | Toolchain `std::priority_queue`; review signatures, allocation and semantics at call sites |
| `queue` | 1 | Toolchain `std::queue`; review signatures, allocation and semantics at call sites |
| `random_shuffle` | 3 | std::shuffle with recorded equivalent randomness requirements |
| `rbegin` | 2 | Toolchain `std::rbegin`; review signatures, allocation and semantics at call sites |
| `remove_const` | 6 | Toolchain `std::remove_const`; review signatures, allocation and semantics at call sites |
| `remove_cv_t` | 2 | Toolchain `std::remove_cv_t`; review signatures, allocation and semantics at call sites |
| `remove_cvref_t` | 6 | Toolchain `std::remove_cvref_t`; review signatures, allocation and semantics at call sites |
| `remove_if` | 12 | Toolchain `std::remove_if`; review signatures, allocation and semantics at call sites |
| `remove_pointer_t` | 1 | Toolchain `std::remove_pointer_t`; review signatures, allocation and semantics at call sites |
| `remove_reference` | 16 | Toolchain `std::remove_reference`; review signatures, allocation and semantics at call sites |
| `remove_reference_t` | 3 | Toolchain `std::remove_reference_t`; review signatures, allocation and semantics at call sites |
| `rend` | 4 | Toolchain `std::rend`; review signatures, allocation and semantics at call sites |
| `replace` | 1 | Toolchain `std::replace`; review signatures, allocation and semantics at call sites |
| `result_of_t` | 1 | std::invoke_result_t with adjusted signature |
| `reverse` | 2 | Toolchain `std::reverse`; review signatures, allocation and semantics at call sites |
| `reverse_iterator` | 6 | Toolchain `std::reverse_iterator`; review signatures, allocation and semantics at call sites |
| `rotate` | 4 | Toolchain `std::rotate`; review signatures, allocation and semantics at call sites |
| `search` | 4 | Toolchain `std::search`; review signatures, allocation and semantics at call sites |
| `set` | 26 | Toolchain `std::set`; review signatures, allocation and semantics at call sites |
| `set_difference_2` | 1 | Review comparator arity and use standard algorithm/Nau adapter |
| `set_intersection` | 1 | Toolchain `std::set_intersection`; review signatures, allocation and semantics at call sites |
| `shared_ptr` | 170 | Toolchain `std::shared_ptr`; review signatures, allocation and semantics at call sites |
| `size` | 1 | Toolchain `std::size`; review signatures, allocation and semantics at call sites |
| `sort` | 32 | Toolchain `std::sort`; review signatures, allocation and semantics at call sites |
| `sort_heap` | 1 | Toolchain `std::sort_heap`; review signatures, allocation and semantics at call sites |
| `span` | 580 | Toolchain `std::span`; review signatures, allocation and semantics at call sites |
| `stable_sort` | 1 | Toolchain `std::stable_sort`; review signatures, allocation and semantics at call sites |
| `stack` | 8 | Toolchain `std::stack`; review signatures, allocation and semantics at call sites |
| `string` | 1530 | Toolchain `std::string`; review signatures, allocation and semantics at call sites |
| `string_view` | 793 | Toolchain `std::string_view`; review signatures, allocation and semantics at call sites |
| `swap` | 106 | Toolchain `std::swap`; review signatures, allocation and semantics at call sites |
| `tie` | 11 | Toolchain `std::tie`; review signatures, allocation and semantics at call sites |
| `to_string` | 23 | Toolchain `std::to_string`; review signatures, allocation and semantics at call sites |
| `to_underlying` | 54 | C++20 Nau enum helper |
| `transform` | 14 | Toolchain `std::transform`; review signatures, allocation and semantics at call sites |
| `true_type` | 19 | Toolchain `std::true_type`; review signatures, allocation and semantics at call sites |
| `tuple` | 35 | Toolchain `std::tuple`; review signatures, allocation and semantics at call sites |
| `tuple_element` | 4 | Toolchain `std::tuple_element`; review signatures, allocation and semantics at call sites |
| `tuple_size` | 3 | Toolchain `std::tuple_size`; review signatures, allocation and semantics at call sites |
| `tuple_vector` | 9 | DESIGN GAP: structure-of-arrays storage, indexed columns and coordinated row lifetime |
| `type_select` | 11 | std::conditional after checking arity |
| `u16string` | 7 | Toolchain `std::u16string`; review signatures, allocation and semantics at call sites |
| `u16string_view` | 3 | Toolchain `std::u16string_view`; review signatures, allocation and semantics at call sites |
| `u32string` | 50 | Toolchain `std::u32string`; review signatures, allocation and semantics at call sites |
| `u32string_view` | 3 | Toolchain `std::u32string_view`; review signatures, allocation and semantics at call sites |
| `u8string` | 36 | Toolchain `std::u8string`; review signatures, allocation and semantics at call sites |
| `u8string_view` | 62 | Toolchain `std::u8string_view`; review signatures, allocation and semantics at call sites |
| `underlying_type` | 13 | Toolchain `std::underlying_type`; review signatures, allocation and semantics at call sites |
| `underlying_type_t` | 21 | Toolchain `std::underlying_type_t`; review signatures, allocation and semantics at call sites |
| `uninitialized_copy_ptr` | 9 | std::uninitialized_copy |
| `uninitialized_default_fill_n` | 1 | std::uninitialized_default_construct_n; check initialization contract |
| `uninitialized_fill_n_ptr` | 10 | std::uninitialized_fill_n |
| `uninitialized_move_ptr` | 6 | std::uninitialized_move |
| `uninitialized_move_ptr_if_noexcept` | 9 | Nau move-if-noexcept uninitialized algorithm with correct cleanup |
| `unique` | 4 | Toolchain `std::unique`; review signatures, allocation and semantics at call sites |
| `unique_ptr` | 299 | Toolchain `std::unique_ptr`; review signatures, allocation and semantics at call sites |
| `unordered_map` | 80 | Toolchain `std::unordered_map`; review signatures, allocation and semantics at call sites |
| `unordered_set` | 25 | Toolchain `std::unordered_set`; review signatures, allocation and semantics at call sites |
| `upper_bound` | 2 | Toolchain `std::upper_bound`; review signatures, allocation and semantics at call sites |
| `use_self` | 2 | std::identity |
| `variant` | 28 | Toolchain `std::variant`; review signatures, allocation and semantics at call sites |
| `vector` | 1213 | Toolchain `std::vector`; review signatures, allocation and semantics at call sites |
| `vector_map` | 31 | Nau sorted contiguous unique-key map |
| `vector_multimap` | 1 | Nau sorted contiguous map; retain duplicate keys and equal_range |
| `vector_multiset` | 4 | Nau sorted contiguous set; retain duplicate values and equal_range |
| `vector_set` | 40 | Nau sorted contiguous unique-key set |
| `visit` | 43 | Toolchain `std::visit`; review signatures, allocation and semantics at call sites |
| `void_t` | 2 | Toolchain `std::void_t`; review signatures, allocation and semantics at call sites |
| `weak_ptr` | 12 | Toolchain `std::weak_ptr`; review signatures, allocation and semantics at call sites |
| `wstring` | 17 | Toolchain `std::wstring`; review signatures, allocation and semantics at call sites |
| `wstring_view` | 20 | Toolchain `std::wstring_view`; review signatures, allocation and semantics at call sites |
| `yes_type` | 14 | Replace detection helper with std::true_type; review sizeof-based consumers |

## Independent EABase users

- `NauEngineLite/engine/core/modules/dagorECS/include/daECS/core/event.h`
- `NauSamples/all3rdpartyBuild/main.cpp`

EABase therefore cannot be deleted solely because EASTL is removed. Recheck these consumers and EA macros after migration.

Section 6 recheck: the Dagor event header now uses standard `constexpr`, and the sample sanity target uses `<cstddef>` for `nullptr_t`. The active source/interface audit finds no remaining EABase import, and clean minimal and desktop configurations contain no EABase target. EABase can therefore be removed alongside EASTL; its original files are retained only in the ignored migration baseline for reversibility.

## Integration surfaces

- Kernel public headers, aliases, strings, reflection and serializer overloads; see per-file inventory.
- Renderer, graphics and Dagor ECS include optional/inactive sources as well as built targets.
- Editor engine bridges, NauSamples shared/sample code, NauDemo native/Web entry points.
- Full/minimal dependency lists, kernel linkage, preset definitions, SDK imports/exports and generated project templates.
- Browser EASTL debug-break implementation and native EASTL allocation hooks.

## Design gap found during inventory

The existing design covers inline vectors/strings, unique sorted containers, dynamic bits, intrusive lists and relocation. It does not specify tuple-vector column layout, fixed-map node pools, copyable fixed callbacks, intrusive reference-count ownership or LRU eviction. Concrete consumers include ECS `internal/eventsDb.h`, `internal/archetypes.h`, and `ecsQuery.h`; graphics `daBfg/frontend/internalRegistry.h`; renderer `dag_resourcePool.h` and `shadersBinaryData.h`. Extend design/spec scenarios/tasks before implementing these replacements. Ordered multimap/multiset replacements must preserve duplicates, not inherit the unique-container requirement.


## Section 5 resolved desktop mappings

Ordinary module/tool sequences, strings, optional/variant, algorithms, ownership and callbacks now use the toolchain STL. Raw renderer byte consumers use Nau HeapByteAllocator (checked byte sizing/alignment and paired free); typed frame/stack consumers use the typed resource adapters. Contiguous Boolean ECS components retain dag::Vector<bool>, not proxy-based std::vector<bool>. Graphics string-view lookup uses transparent Nau StringHash with std::equal_to<>; asset keys retain their transparent AssetPath hash. Persistent ECS hashes are unchanged.

ECS archetype storage boxes standard string/list/object/array/shared owners and relocates only the pointer slots. This deliberately trades extra boxing allocations for correct standard object lifetimes; the old explicit byte-relocatable classification is invalid for these owners. Retained Dagor raw relocation is limited to its reviewed POD/custom relocatable values. Render fixed bits use std::bitset with the required scan adapter. Bundled ska and Cocos integration patches are documented in third-party-patches.md.

The default Windows graph covers physics/Jolt, input/gainput, network, audio, Lua, app framework, DX12 and tools. Existing disabled Dagor net sources and commented input/UI/platform test hookups remain outside the supported graph; their lexical migration is not a runtime validation claim. Apple/Android Cocos source changes are likewise not platform build claims. CMake EASTL links/exports and external editor/sample/demo/template consumers remain for section 6.
