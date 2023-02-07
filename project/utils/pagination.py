from django.core.paginator import Page


class PaginationMixin:

    def get_pages(self, **kwargs) -> dict:
        """Prettifying pagination view by sing elided page_range"""
        context = kwargs
        page: Page = context.get("page_obj")
        if page is not None:
            context.update(
                pages=page.paginator.get_elided_page_range(
                    number=page.number,
                    on_each_side=1,
                    on_ends=1
                )
            )

        return context
